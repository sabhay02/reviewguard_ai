import os
from arq.connections import RedisSettings
from app.services.review_service import ReviewService

import asyncio

async def _run_review_async(ctx, repo_url: str, pr_number: int):
    """Background task processed by ARQ worker."""
    service = ReviewService()
    try:
        print(f"[Worker] Starting review for PR #{pr_number}...")
        # Run the heavy synchronous AI graph in a separate thread!
        await asyncio.to_thread(service.review_pull_request, repo_url, pr_number, "webhook")
        print(f"[Worker] Finished review for PR #{pr_number}!")
    except Exception as exc:
        print(f"[Worker] Review failed for PR #{pr_number}: {exc}")


class WorkerSettings:
    functions = [_run_review_async]
    redis_settings = RedisSettings(host=os.getenv("REDIS_HOST", "localhost"), port=6379)
