from models.base import BaseModel
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,INTEGER,ForeignKey
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
    created_by:Mapped[str] = mapped_column(
        ForeignKey("users.id")
    )