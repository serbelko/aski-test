from fastapi import APIRouter
from src.schemas.base_scheme import ChatRequest

router = APIRouter()


@router.get("/ping", tags=["Health"])
async def ping():
    """
    Health check endpoint.
    """
    return {"message": "pong"}


@router.post("/process_chat/")
async def process_chat(data: ChatRequest):
    return {
        "message": "Данные получены успешно",
        "chat_id": data.chat_id,
        "organization_id": data.organization_id
    }