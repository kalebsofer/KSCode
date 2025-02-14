import os
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from model_loader import ModelLoader
from typing import Optional, List, Dict
from uuid import uuid4

app = FastAPI()


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.6


# Session management
sessions: Dict[str, List[ChatMessage]] = {}


def get_model_loader():
    model_path = os.getenv("MODEL_PATH", "/models/DeepSeek-R1-Distill-Qwen-7B")
    loader = ModelLoader(model_path)
    loader.load_model()
    return loader


def get_session(session_id: Optional[str] = None):
    if session_id is None:
        session_id = str(uuid4())
    if session_id not in sessions:
        sessions[session_id] = []
    return session_id, sessions[session_id]


@app.post("/chat")
async def chat(
    request: ChatRequest,
    model_loader: ModelLoader = Depends(get_model_loader),
    session: tuple[str, list] = Depends(get_session),
):
    session_id, history = session
    try:
        # Combine history with new messages
        full_conversation = history + request.messages

        # Generate response
        response = model_loader.generate_chat(
            full_conversation, request.max_tokens, request.temperature
        )

        # Update session history
        history.extend(request.messages)
        history.append(ChatMessage(role="assistant", content=response))

        return {"session_id": session_id, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Add CORS middleware if needed
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
