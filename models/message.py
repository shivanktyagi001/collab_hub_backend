from models.base import BaseModel
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey,String,Text,Boolean

class Message(BaseModel):
    __tablename__ = "messages"
    channel_id : Mapped[int]= mapped_column(
        ForeignKey("channels.id"),
        nullable=False
    )
    sender_id : Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    
    content:Mapped[str]=mapped_column(
        Text,
        nullable=False
    )
    edited:Mapped[bool]=mapped_column(
        Boolean,
        default=False
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    channel = relationship(
        "Channel",
        back_populates="messages"
    )
    sender = relationship(
        "User",
        back_populates="messages"
    )
    

