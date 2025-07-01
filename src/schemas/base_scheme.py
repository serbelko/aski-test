from pydantic import BaseModel


class ChatRequest(BaseModel):
    chat_id: int
    organization_id: str