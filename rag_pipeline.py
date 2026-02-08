from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    String, Integer, Float, text
)

# LlamaIndex
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, Document, VectorStoreIndex
from llama_index.core.query_engine import NLSQLTableQueryEngine, RouterQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core import SQLDatabase

import nest_asyncio
nest_asyncio.apply()

# Globals
_INITIALIZED = False
_engine = None
_router = None


# --------------------------------------------------------------------------
# 1. LOAD CSV → DuckDB
# --------------------------------------------------------------------------
def _ensure_tables(engine):
    print("🔄 Loading CSV files...")

    folder = Path("data/ingres")
    if not folder.exists():
        raise RuntimeError("❌ Folder data/ingres does NOT exist")

    pattern = str(folder / "*.csv")
    if not any(folder.glob("*.csv")):
        raise RuntimeError("❌ No CSV files found in data/ingres/*.csv")

    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS assessments;"))
        conn.execute(text(f"""
            CREATE TABLE assessments AS
            SELECT * FROM read_csv_auto(
                '{pattern}',
                HEADER=TRUE,
                UNION_BY_NAME=TRUE
            );
        """))

        count = conn.execute(text("SELECT COUNT(*) FROM assessments")).scalar()
        print(f"✅ Loaded {count} rows into assessments")


# --------------------------------------------------------------------------
# 2. NO REFLECTION — Build Metadata by Hand
# --------------------------------------------------------------------------
def _build_metadata(engine):
    metadata = MetaData()

    with engine.begin() as conn:
        rows = conn.execute(text("PRAGMA table_info('assessments')")).fetchall()

    cols = []
    for _, name, dtype, *_ in rows:
        dtype = dtype.upper()

        if "INT" in dtype:
            cols.append(Column(name, Integer))
        elif "DOUBLE" in dtype or "FLOAT" in dtype:
            cols.append(Column(name, Float))
        else:
            cols.append(Column(name, String))

    table = Table("assessments", metadata, *cols)
    return metadata, table


# --------------------------------------------------------------------------
# 3. INITIALIZE MODELS (ASYNC-SAFE)
# --------------------------------------------------------------------------
async def _init_models():
    global _INITIALIZED
    if _INITIALIZED:
        return

    load_dotenv()

    key = (
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
    )
    if not key:
        raise RuntimeError("❌ No Gemini API key found")

    os.environ["GOOGLE_API_KEY"] = key
    print("🔑 Gemini API key loaded")

    # FIXED: Use the ASYNC Google LLM
    # Using gemini-2.5-flash (Gemini 1.5 models were shut down Sept 2025)
    Settings.llm = GoogleGenAI(
        model="gemini-2.5-flash",
        api_key=key,
        use_async=True
    )

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    print("🤖 Models initialized")
    _INITIALIZED = True


# --------------------------------------------------------------------------
# 4. BUILD ROUTER — NO REFLECTION AT ALL
# --------------------------------------------------------------------------
async def build_router():
    global _engine, _router

    await _init_models()

    if _engine is None:
        _engine = create_engine("duckdb:///ingres.duckdb")
        _ensure_tables(_engine)

    # Build metadata manually
    metadata, table = _build_metadata(_engine)

    # Create SQLDatabase with the pre-built metadata
    sql_db = SQLDatabase(
        _engine,
        metadata=metadata,
        include_tables=["assessments"]
    )

    base_sql = NLSQLTableQueryEngine(
        sql_database=sql_db,
        tables=["assessments"]
    )

    class SafeSQLEngine:
        def __init__(self, inner):
            self.inner = inner

        async def aquery(self, q):
            return await self.inner.aquery(
                str(q) + "\n-- Use ONLY assessments table. No JOINs.\n"
            )

    sql_tool = QueryEngineTool.from_defaults(
        query_engine=SafeSQLEngine(base_sql),
        description="SQL tool for querying groundwater"
    )

    glossary = [Document(text="Groundwater categories: safe, semi_critical, critical, over_exploited.")]
    vect_engine = VectorStoreIndex.from_documents(glossary).as_query_engine()

    vect_tool = QueryEngineTool.from_defaults(
        query_engine=vect_engine,
        description="Definition lookups"
    )

    _router = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[sql_tool, vect_tool]
    )

    return _router


# --------------------------------------------------------------------------
# PUBLIC API
# --------------------------------------------------------------------------
async def get_router():
    global _router
    if _router is None:
        _router = await build_router()
    return _router


async def aquery(q: str) -> Dict[str, Any]:
    router = await get_router()
    res = await router.aquery(q)
    return {
        "response": str(res),
        "sql_query": res.metadata.get("sql_query") if hasattr(res, "metadata") else None
    }
