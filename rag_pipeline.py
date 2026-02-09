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
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, Document, VectorStoreIndex
from llama_index.core.query_engine import NLSQLTableQueryEngine, RouterQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core import SQLDatabase
from llama_index.core.prompts import PromptTemplate

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

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise RuntimeError("❌ No Groq API key found")

    print("🔑 Groq API key loaded")

    # Using Groq with Llama 3.3 70B (latest model)
    Settings.llm = Groq(
        model="llama-3.3-70b-versatile",
        api_key=groq_key
    )

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    print("🤖 Models initialized (Groq + Llama 3.1)")
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

    # Enhanced text-to-SQL prompt with examples for tricky numerical queries
    text_to_sql_prompt = PromptTemplate(
        "Given an input question, create a syntactically correct SQL query to run.\n\n"
        "DATABASE SCHEMA:\n"
        "Table: assessments\n"
        "Columns:\n"
        "- place (VARCHAR): district or city name\n"
        "- state (VARCHAR): Indian state name (e.g., 'Madhya Pradesh', 'Bihar', 'Rajasthan')\n"
        "- rainfall (FLOAT): annual rainfall in mm\n"
        "- groundwater_refilled_total (FLOAT): total groundwater recharged\n"
        "- groundwater_used_total (FLOAT): total groundwater extracted/used\n"
        "- groundwater_status (VARCHAR): 'safe', 'semi_critical', 'critical', 'over_exploited'\n"
        "- land_total (FLOAT): total land area\n"
        "- land_nonirrigated (FLOAT): non-irrigated land area\n"
        "- land_irrigated (FLOAT): irrigated land area\n"
        "- year (INTEGER): assessment year (2021-2024)\n\n"
        "CRITICAL RULES:\n"
        "1. Status values are LOWERCASE: 'safe', 'semi_critical', 'critical', 'over_exploited'\n"
        "2. For 'sustainably managed' or 'safe' → use groundwater_status = 'safe'\n"
        "3. For 'over-exploited' → use groundwater_status = 'over_exploited'\n"
        "4. State names are case-sensitive: 'Madhya Pradesh', 'Bihar', 'Rajasthan', etc.\n"
        "5. Use ONLY the 'assessments' table. No JOINs.\n"
        "6. For calculations, use proper SQL functions: SUM(), AVG(), COUNT(), MAX(), MIN()\n"
        "7. For percentages, multiply by 100.0 to avoid integer division\n"
        "8. For comparisons between columns, use proper arithmetic operators\n\n"
        "EXAMPLE QUERIES:\n\n"
        "Q: Which areas use more groundwater than they refill?\n"
        "A: SELECT place, state, groundwater_used_total, groundwater_refilled_total \n"
        "   FROM assessments \n"
        "   WHERE groundwater_used_total > groundwater_refilled_total;\n\n"
        "Q: What is the average rainfall in Madhya Pradesh?\n"
        "A: SELECT AVG(rainfall) as avg_rainfall FROM assessments WHERE state = 'Madhya Pradesh';\n\n"
        "Q: Show top 5 districts with highest groundwater usage\n"
        "A: SELECT place, state, SUM(groundwater_used_total) as total_usage \n"
        "   FROM assessments \n"
        "   GROUP BY place, state \n"
        "   ORDER BY total_usage DESC LIMIT 5;\n\n"
        "Q: Count how many areas are over-exploited in each state\n"
        "A: SELECT state, COUNT(*) as count \n"
        "   FROM assessments \n"
        "   WHERE groundwater_status = 'over_exploited' \n"
        "   GROUP BY state ORDER BY count DESC;\n\n"
        "Q: What percentage of land is irrigated in Bihar?\n"
        "A: SELECT (SUM(land_irrigated) * 100.0 / SUM(land_total)) as irrigation_percentage \n"
        "   FROM assessments WHERE state = 'Bihar';\n\n"
        "Q: Which areas have rainfall above 1500mm and are still over-exploited?\n"
        "A: SELECT place, state, rainfall, groundwater_status \n"
        "   FROM assessments \n"
        "   WHERE rainfall > 1500 AND groundwater_status = 'over_exploited';\n\n"
        "Q: Compare groundwater usage vs refill for Rajasthan\n"
        "A: SELECT SUM(groundwater_used_total) as total_used, \n"
        "          SUM(groundwater_refilled_total) as total_refilled,\n"
        "          (SUM(groundwater_used_total) - SUM(groundwater_refilled_total)) as deficit\n"
        "   FROM assessments WHERE state = 'Rajasthan';\n\n"
        "Q: Show areas where usage is more than 80% of refill\n"
        "A: SELECT place, state, groundwater_used_total, groundwater_refilled_total,\n"
        "          (groundwater_used_total * 100.0 / groundwater_refilled_total) as usage_percent\n"
        "   FROM assessments \n"
        "   WHERE groundwater_refilled_total > 0 \n"
        "   AND (groundwater_used_total * 100.0 / groundwater_refilled_total) > 80;\n\n"
        "Q: What's the trend of safe areas from 2021 to 2024?\n"
        "A: SELECT year, COUNT(*) as safe_count \n"
        "   FROM assessments \n"
        "   WHERE groundwater_status = 'safe' \n"
        "   GROUP BY year ORDER BY year;\n\n"
        "IMPORTANT: Return ONLY the SQL query, with NO explanations, NO markdown, NO additional text.\n"
        "Just the raw SQL query that can be executed directly.\n\n"
        "Question: {query_str}\n"
        "SQL Query:"
    )

    # Create the SQL query engine
    # Note: By default, NLSQLTableQueryEngine will execute the SQL and synthesize a response
    # The key is to ensure the text-to-SQL prompt returns ONLY the SQL query, not explanations
    base_sql = NLSQLTableQueryEngine(
        sql_database=sql_db,
        tables=["assessments"],
        text_to_sql_prompt=text_to_sql_prompt
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
        description=(
            "SQL tool for querying groundwater assessment data. "
            "The 'assessments' table has these columns: "
            "place (district/city name), state (Indian state name), "
            "rainfall, groundwater_refilled_total, groundwater_used_total, "
            "groundwater_status (MUST be one of: 'safe', 'semi_critical', 'critical', 'over_exploited'), "
            "land_total, land_nonirrigated, land_irrigated, year. "
            "IMPORTANT: Use the 'state' column to filter by Indian states like 'Madhya Pradesh', 'Bihar', 'Rajasthan', etc. "
            "IMPORTANT: For sustainably managed groundwater, use groundwater_status = 'safe' (lowercase). "
            "IMPORTANT: The status values are lowercase: 'safe', 'semi_critical', 'critical', 'over_exploited'."
        )
    )

    glossary = [
        # Basic definitions
        Document(text="Groundwater categories: safe (sustainably managed), semi_critical, critical, over_exploited."),
        Document(text="The database contains groundwater data for 22 Indian states including Madhya Pradesh, Bihar, Rajasthan, Maharashtra, etc."),
        Document(text="Data covers years 2021-2024 with measurements of rainfall, groundwater refill, groundwater usage, and land statistics."),

        # Status values
        Document(text="IMPORTANT: groundwater_status values are ALWAYS lowercase: 'safe', 'semi_critical', 'critical', 'over_exploited'. Never use capitalized versions."),

        # Basic filtering examples
        Document(text="Example: Find safe areas in Madhya Pradesh → SELECT place FROM assessments WHERE state = 'Madhya Pradesh' AND groundwater_status = 'safe'"),
        Document(text="Example: Find over-exploited areas in Rajasthan → SELECT place FROM assessments WHERE state = 'Rajasthan' AND groundwater_status = 'over_exploited'"),

        # Numerical comparisons
        Document(text="Example: Areas using more water than refilled → SELECT place, state FROM assessments WHERE groundwater_used_total > groundwater_refilled_total"),
        Document(text="Example: High rainfall areas (>1500mm) → SELECT place, state, rainfall FROM assessments WHERE rainfall > 1500"),

        # Aggregations
        Document(text="Example: Average rainfall by state → SELECT state, AVG(rainfall) FROM assessments GROUP BY state"),
        Document(text="Example: Count areas by status → SELECT groundwater_status, COUNT(*) FROM assessments GROUP BY groundwater_status"),
        Document(text="Example: Total groundwater usage by state → SELECT state, SUM(groundwater_used_total) FROM assessments GROUP BY state"),

        # Percentages and ratios
        Document(text="Example: Calculate usage percentage → SELECT place, (groundwater_used_total * 100.0 / groundwater_refilled_total) as usage_percent FROM assessments WHERE groundwater_refilled_total > 0"),
        Document(text="Example: Irrigation percentage → SELECT state, (SUM(land_irrigated) * 100.0 / SUM(land_total)) as irrigation_pct FROM assessments GROUP BY state"),

        # Top/Bottom queries
        Document(text="Example: Top 10 highest rainfall areas → SELECT place, state, rainfall FROM assessments ORDER BY rainfall DESC LIMIT 10"),
        Document(text="Example: Areas with lowest groundwater refill → SELECT place, state, groundwater_refilled_total FROM assessments ORDER BY groundwater_refilled_total ASC LIMIT 10"),

        # Year-based trends
        Document(text="Example: Trend of safe areas over years → SELECT year, COUNT(*) FROM assessments WHERE groundwater_status = 'safe' GROUP BY year ORDER BY year"),
        Document(text="Example: Compare 2021 vs 2024 → SELECT year, AVG(rainfall), AVG(groundwater_used_total) FROM assessments WHERE year IN (2021, 2024) GROUP BY year"),

        # Complex conditions
        Document(text="Example: Critical areas with high usage → SELECT place, state FROM assessments WHERE groundwater_status IN ('critical', 'over_exploited') AND groundwater_used_total > 5000"),
        Document(text="Example: Safe areas with low rainfall → SELECT place, state, rainfall FROM assessments WHERE groundwater_status = 'safe' AND rainfall < 800")
    ]
    vect_engine = VectorStoreIndex.from_documents(glossary).as_query_engine()

    vect_tool = QueryEngineTool.from_defaults(
        query_engine=vect_engine,
        description="Definition lookups for groundwater terminology and database schema"
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

    # Extract SQL query from metadata for debugging
    sql_query = res.metadata.get("sql_query") if hasattr(res, "metadata") else None
    if sql_query:
        print(f"🔍 Generated SQL: {sql_query}")

    return {
        "response": str(res),
        "sql_query": sql_query
    }
