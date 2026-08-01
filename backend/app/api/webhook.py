import hashlib
import hmac

from fastapi import APIRouter, Depends, Header, HTTPException, Request

async def rate_limit(request: Request):
    """Simple fixed-window Redis rate limiter."""
    redis_client = request.app.state.redis
    client_ip = request.client.host if request.client else "unknown"
    key = f"rate_limit:{client_ip}"
    
    requests = await redis_client.incr(key)
    if requests == 1:
        await redis_client.expire(key, 60)
    if requests > 10:
        raise HTTPException(status_code=429, detail="Too many requests")


from app.github.parser import extract_pr_info
from app.services.review_service import ReviewService
from app.utils.configs import settings

router = APIRouter(prefix="/github")

service = ReviewService()


def _verify_signature(payload_bytes: bytes, signature: str | None) -> bool:
    """Verify X-Hub-Signature-256 from GitHub to reject forged payloads."""
    secret = getattr(settings, "GITHUB_WEBHOOK_SECRET", None)

    # If no secret configured, skip verification (dev mode)
    if not secret:
        return True

    if not signature or not signature.startswith("sha256="):
        return False

    mac = hmac.new(
        secret.encode("utf-8"), payload_bytes, hashlib.sha256
    )
    expected = "sha256=" + mac.hexdigest()

    return hmac.compare_digest(expected, signature)


@router.post(
    "/webhook",
    dependencies=[Depends(rate_limit)],
)
async def github_webhook(
    request: Request,
    x_github_event: str | None = Header(default=None, alias="X-GitHub-Event"),
    x_hub_signature_256: str | None = Header(
        default=None, alias="X-Hub-Signature-256"
    ),
):
    payload_bytes = await request.body()

    # --- Signature verification ---
    if not _verify_signature(payload_bytes, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    payload = await request.json()

    print(f"[Webhook] Event: {x_github_event}")

    # Only handle pull_request events
    if x_github_event != "pull_request":
        return {"status": "ignored", "reason": f"event '{x_github_event}' not handled"}

    action = payload.get("action", "")

    # Trigger on open or new push to PR branch
    if action not in ("opened", "synchronize", "reopened"):
        return {"status": "ignored", "reason": f"action '{action}' not handled"}

    info = extract_pr_info(payload)
    print(f"[Webhook] PR #{info.get('pr_number')} — {action} — {info.get('repo_url')}")

    # Fire review as an ARQ background task so we return 200 immediately
    arq_pool = request.app.state.arq_pool
    await arq_pool.enqueue_job(
        "_run_review_async",
        repo_url=info["repo_url"],
        pr_number=info["pr_number"],
    )

    return {
        "status": "accepted",
        "pr_number": info.get("pr_number"),
        "action": action,
    }