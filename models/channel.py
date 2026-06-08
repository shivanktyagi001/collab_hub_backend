from models.base import BaseModel
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,INTEGER,ForeignKey,Boolean
class Channel(BaseModel):
    __tablename__ = "channels"
    workspace_id:Mapped[int]=mapped_column(
        ForeignKey("workspaces.id")
    )
    name:Mapped[str] = mapped_column(
        String(100)
    )
    desc : Mapped[str] = mapped_column(
        String(300)
    )
    created_by:Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    is_private:Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    workspace = relationship(
        "Workspace",
        back_populates="channels"
    )
    creator = relationship(
        "User",
        back_populates="created_channels"
    )
    messages = relationship(
        "Message",
        back_populates="channel",
        cascade="all,delete-orphan"
    )
    
    