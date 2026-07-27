import hashlib
import hmac

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request

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


def _run_review(repo_url: str, pr_number: int) -> None:
    """Background task — runs the full multi-agent review pipeline."""
    try:
        service.review_pull_request(repo_url, pr_number, source="webhook")
    except Exception as exc:  # noqa: BLE001
        print(f"[Webhook] Review failed for PR #{pr_number}: {exc}")


@router.post("/webhook")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
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

    # Fire review as a background task so we return 200 immediately
    background_tasks.add_task(
        _run_review,
        repo_url=info["repo_url"],
        pr_number=info["pr_number"],
    )

    return {
        "status": "accepted",
        "pr_number": info.get("pr_number"),
        "action": action,
    }