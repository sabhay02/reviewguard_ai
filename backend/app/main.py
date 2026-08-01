from contextlib import asynccontextmanager
import os
import redis.asyncio as redis
from arq import create_pool
from arq.connections import RedisSettings

from fastapi import FastAPI

from app.api.webhook import router as webhook_router
from app.api.review import router as review_router
from app.api.health import router as health_router
from app.api.dashboard import router as dashboard_router
from app.api.chat import router as chat_router
from app.database.history import initialize_db
from app.graphs.check import _stack
from app.rag.ingest import ingest_knowledge
from app.api.auth import verify_api_key
from fastapi import Depends


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────
    redis_url = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:6379/0"
    app.state.redis = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    app.state.arq_pool = await create_pool(RedisSettings(host=os.getenv("REDIS_HOST", "localhost"), port=6379))
    print("[Startup] Redis & ARQ Pool initialized.")

    initialize_db()          # ensure reviews table exists
    print("[Startup] Database initialized.")
    ingest_knowledge()       # index knowledge/*.md docs into ChromaDB
    print("[Startup] Knowledge base indexed.")
    yield
    # ── Shutdown ─────────────────────────────────────────
    _stack.close()           # cleanly close SQLite checkpointer
    print("[Shutdown] Checkpointer closed.")


app = FastAPI(
    title="ReviewGuard AI",
    version="0.1.0",
    lifespan=lifespan,
)

from fastapi.middleware.cors import CORSMiddleware

import os

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(webhook_router) # Webhook uses its own GitHub HMAC signature
app.include_router(review_router, dependencies=[Depends(verify_api_key)])
app.include_router(dashboard_router, dependencies=[Depends(verify_api_key)])
app.include_router(chat_router, dependencies=[Depends(verify_api_key)])


@app.get("/")
def root():
    return {"message": "ReviewGuard AI is running 🚀"}