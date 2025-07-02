from fastapi import APIRouter, HTTPException
from src.schemas.base_scheme import ChatRequest
from src.servises.send_promt import get_gemini_answer
router = APIRouter()


@router.get("/ping", tags=["Health"])
async def ping():
    """
    Health check endpoint.
    """
    return {"message": "pong"}


@router.post("/process_chat/")
async def process_chat(data: ChatRequest):

    asnswer = get_gemini_answer(organization_id=data.organization_id)
    if asnswer == 'Index Error':
        raise HTTPException(status_code=404, detail="Компания не найдена")
    print(asnswer)
    return {
            "message": "Данные получены и отправлены успешно",
            "chat_id": data.chat_id,
            "organization_id": data.organization_id
        }

