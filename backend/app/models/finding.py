from pydantic import BaseModel, Field
from typing import Optional


class AIReview(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    impact: Optional[str] = None
    recommendation: Optional[str] = None
    secure_code: Optional[str] = None
    status: Optional[str] = None


class Finding(BaseModel):
    agent: str = ""
    tool: str
    rule: str

    severity: str
    confidence: Optional[str] = None

    file: str
    line: int

    message: str

    review: AIReview = Field(default_factory=AIReview)