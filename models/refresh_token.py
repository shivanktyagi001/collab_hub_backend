from sqlalchemy import String,DateTime,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from models.base import BaseModel
from datetime import datetime
class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"
    user_id: Mapped[int]=mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    token_hash : Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )
    expires_at :Mapped[datetime]=mapped_column(
        DateTime,
        nullable=False,
    )
    revoked:Mapped[bool]=mapped_column(
        default=False
    )
    user = relationship(
        "User",
        back_populates="refresh_tokens"
    )