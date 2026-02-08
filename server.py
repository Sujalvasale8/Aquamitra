from __future__ import annotations

import time
from typing import List, Optional
import traceback

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import rag_pipeline
from translation_service import (
    translate_query_to_english,
    translate_response_to_language,
    SUPPORTED_LANGUAGES,
)

from sqlalchemy import text

app = FastAPI(title="Groundwater RAG Assistant", version="0.1.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request & Response Models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    stream: Optional[bool] = False
    session_id: Optional[str] = None
    language: Optional[str] = "en"

class ChatResponse(BaseModel):
    response: str
    sql_query: Optional[str] = None
    latency_ms: int
    original_query: Optional[str] = None
    translated_query: Optional[str] = None


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/languages")
def get_supported_languages():
    return {"languages": SUPPORTED_LANGUAGES}


# ------------------------------
# MAIN CHAT ENDPOINT (ASYNC)
# ------------------------------
@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="messages cannot be empty")

    user_language = req.language or "en"
    user_message = req.messages[-1].content.strip()

    original_query = user_message
    translated_query = user_message
    start = time.perf_counter()

    try:
        # 1. Translate input
        if user_language != "en":
            translated_query = translate_query_to_english(user_message, user_language)

        # 2. Run RAG async
        try:
            result = await rag_pipeline.aquery(translated_query)
        except Exception:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="RAG Pipeline Error")

        # 3. Translate back
        if user_language != "en":
            result["response"] = translate_response_to_language(result["response"], user_language)

        latency_ms = int((time.perf_counter() - start) * 1000)

        # 4. Log to DuckDB
        try:
            engine = rag_pipeline._engine
            with engine.begin() as conn:
                sid = req.session_id or "default"

                conn.execute(text("""
                    INSERT INTO chat_logs (session_id, role, content, sql_query, latency_ms)
                    VALUES (:sid, 'user', :content, NULL, NULL)
                """), {"sid": sid, "content": original_query})

                conn.execute(text("""
                    INSERT INTO chat_logs (session_id, role, content, sql_query, latency_ms)
                    VALUES (:sid, 'assistant', :content, :sql, :lat)
                """), {
                    "sid": sid,
                    "content": result["response"],
                    "sql": result.get("sql_query"),
                    "lat": latency_ms
                })
        except Exception as e:
            print(f"⚠ Logging Warning: {e}")

        return ChatResponse(
            response=result["response"],
            sql_query=result.get("sql_query"),
            latency_ms=latency_ms,
            original_query=original_query if user_language != "en" else None,
            translated_query=translated_query if user_language != "en" else None,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# CHAT HISTORY
# ------------------------------
@app.get("/api/history")
def history(
    session_id: str = Query("default"),
    limit: int = Query(50, le=500)
):
    try:
        engine = rag_pipeline._engine
        with engine.begin() as conn:
            rows = conn.exec_driver_sql(
                """
                SELECT session_id, role, content, sql_query, latency_ms, created_at
                FROM chat_logs
                WHERE session_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (session_id, limit),
            ).fetchall()

        messages = [dict(row._mapping) for row in rows]
        return {"messages": list(reversed(messages))}

    except Exception as e:
        print("🔥 ERROR IN /api/history:", e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
