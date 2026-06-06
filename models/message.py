from models.base import BaseModel
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey,String

class Messages(BaseModel):
    __tablename__ = "messages"
    channel_id : Mapped[int]= mapped_column(
        ForeignKey("channels.id")
    )
    sender_id : Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    parent_message_id :Mapped[int]=mapped_column(
        ForeignKey("messages.id")
    )
    content:Mapped[str]=mapped_column(
        String,
    )
    

