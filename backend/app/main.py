from fastapi import FastAPI

from backend.app.api.webhook import router as webhook_router

app = FastAPI(
    title="ReviewGuard AI",
    version="0.1.0"
)

app.include_router(webhook_router)


@app.get("/")
def root():
    return {"message": "ReviewGuard AI"}