from sqlalchemy import String
from models.base import BaseModel
from sqlalchemy.orm import Mapped,mapped_column,relationship

class User(BaseModel):
    __tablename__ = "users"
    username :Mapped[str]=mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    email:Mapped[str]=mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    password_hash :Mapped[str]=mapped_column(
        String(255),
        nullable=False,
    )
    is_active :Mapped[bool]= mapped_column(
        default=True
    )
    is_verified :Mapped[bool]=mapped_column(
        default=False
    )
    refresh_tokens=relationship(
        "RefreshToken",
        back_populates="user"
    )
    workspace_members = relationship(
        "WorkspaceMember",
        back_populates="user",
        cascade="all,delete-orphan"
    )
    workspace = relationship(
        "Workspace",
        back_populates="owner"
    )