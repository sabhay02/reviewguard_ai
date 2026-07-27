from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """Liveness probe — used by Render / Railway / Fly.io."""
    return {"status": "ok", "service": "ReviewGuard AI"}
