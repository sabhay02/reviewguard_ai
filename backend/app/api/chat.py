from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from pathlib import Path

from app.llm.groq import LLMClient

router = APIRouter(
    prefix="/chat",
    tags=["ChatBot"]
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    review_id: str
    message: str
    history: list[ChatMessage] = []

class ChatResponse(BaseModel):
    response: str

llm = LLMClient()

@router.post("/", response_model=ChatResponse)
def chat_with_report(request: ChatRequest):
    # Try to load the report for context
    report_path = Path(f"reports/{request.review_id}.md")
    context = "No specific report context found for this review."
    
    if report_path.exists():
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                context = f.read()
        except Exception as e:
            print(f"Failed to read report {report_path}: {e}")
            
    # Truncate context if it's too massive (Groq limit is usually large enough, but just to be safe)
    if len(context) > 20000:
        context = context[:20000] + "\n...[Report Truncated]..."

    system_prompt = f"""You are ReviewGuard AI, an expert DevSecOps and Application Security assistant.
You are helping the user understand and fix vulnerabilities found in their codebase.

Here is the Security Report generated for their code (use this as context):
{context}

Guidelines:
- STRICT RULE: ONLY answer questions based on the provided Security Report context. Do NOT use outside knowledge or hallucinate details.
- If the user asks a question that is completely unrelated to the report or the project's security, politely decline to answer and state that you can only answer questions related to the security report.
- If they ask how to fix a vulnerability mentioned in the report, explain the concept and provide secure code examples.
- Keep responses friendly, professional, and directly related to software security.
- Do not repeat the entire report. Only reference the parts relevant to the user's question.
"""

    messages = [{"role": "system", "content": system_prompt}]
    
    for msg in request.history:
        # Validate roles
        if msg.role in ["user", "assistant"]:
            messages.append({"role": msg.role, "content": msg.content})
            
    messages.append({"role": "user", "content": request.message})
    
    response_text = llm.chat(messages)
    
    return {"response": response_text}
