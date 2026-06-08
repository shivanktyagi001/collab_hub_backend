from pydantic import BaseModel,Field
from datetime import datetime

class CreateMessageRequest(BaseModel):
    content:str=Field(
        min_length=1,
        max_length=5000,
    )

class UpdateMessageRequest(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=5000,
    )

class MessageResponse(BaseModel):
    id:int
    channel_id:int
    sender_id:int
    content:str
    edited:bool
    is_deleted:bool

    created_at:datetime
    updated_at:datetime

    model_config={
        "from_attributes":True
    }