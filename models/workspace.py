from models.base import BaseModel
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,INTEGER,ForeignKey
class Workspace(BaseModel):
    __tablename__ ="workspaces"

    name: Mapped[str]=mapped_column(
        String(100),
        nullable= False
    ) 
    desc :Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )
    owner_id:Mapped[int]=mapped_column(
        ForeignKey("users.id")
    )
    members = relationship(
        "WorkspaceMember",
        back_populates="workspace",
        cascade="all,delete-orphan"
    )
    owner = relationship(
        "User",
        back_populates="workspace"
    )


    
