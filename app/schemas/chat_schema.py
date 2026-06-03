from typing import Any, Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    route: str
    answer: str
    sql_intent: Optional[str] = None
    sql_result: Optional[Any] = None
    retrieved_docs: Optional[Any] = None