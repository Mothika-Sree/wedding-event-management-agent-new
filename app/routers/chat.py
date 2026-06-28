# app/routes/chat.py

from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.wedding_agent import (
    WeddingAgent
)

router = APIRouter()

agent = WeddingAgent()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(req: ChatRequest):

    return agent.process(
        req.message
    )