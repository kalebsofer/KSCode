import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from model_loader import OpenAIAssistant
from schemas import ChatMessage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_tokens: int = 512
    temperature: float = 0.6


sessions: Dict[str, List[ChatMessage]] = {}
client = OpenAIAssistant()


def get_session(session_id: Optional[str] = None):
    if session_id is None:
        session_id = str(uuid4())
    if session_id not in sessions:
        sessions[session_id] = []
    return session_id, sessions[session_id]


@app.post("/chat")
async def chat(request: ChatRequest, session: tuple[str, list] = Depends(get_session)):
    session_id, history = session
    try:
        full_conversation = history + request.messages
        response = client.generate_chat(
            full_conversation, request.max_tokens, request.temperature
        )
        history.extend(request.messages)
        history.append(ChatMessage(role="assistant", content=response))
        return {"session_id": session_id, "response": response}
    except Exception as e:
        msg = f"Error generating text: {str(e)}"
        raise HTTPException(status_code=500, detail=msg)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
