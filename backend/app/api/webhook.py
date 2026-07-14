from fastapi import APIRouter, Request

router = APIRouter(prefix="/github")
from app.github.parser import extract_pr_info

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    event = request.headers.get("X-GitHub-Event")
    
    info = extract_pr_info(payload)
    print(info)

    print("Event:", event)
    print(payload)

    return {"status": "received"}