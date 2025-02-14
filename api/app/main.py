import os
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from model_loader import ModelLoader
from typing import Optional, List, Dict
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatMessage


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.6


sessions: Dict[str, List[ChatMessage]] = {}


def get_model_loader():
    model_path = os.getenv(
        "MODEL_PATH", os.path.join("..", "models", "DeepSeek-R1-Distill-Qwen-7B")
    )
    loader = ModelLoader(model_path)
    loader.load_model()
    return loader


app.state.model_loader = get_model_loader()


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
        full_conversation = history + request.messages

        response = model_loader.generate_chat(
            full_conversation, request.max_tokens, request.temperature
        )

        history.extend(request.messages)
        history.append(ChatMessage(role="assistant", content=response))

        return {"session_id": session_id, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
