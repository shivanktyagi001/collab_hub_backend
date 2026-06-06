from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,ForeignKey,DateTime,Enum as SQLEnum
from models.base import BaseModel
from datetime import datetime
from enum import Enum
class WorkspaceRole(str,Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class WorkspaceMember(BaseModel):
    __tablename__ = "workspace_members"
    workspace_id:Mapped[int]=mapped_column(
        ForeignKey("workspaces.id")
    )
    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id")
    )
    role : Mapped[WorkspaceRole]=mapped_column(
        SQLEnum(WorkspaceRole),
        default=WorkspaceRole.MEMBER
    )
    joined_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    workspace = relationship(
        "Workspace",
        back_populates="members"
    )
    user = relationship(
        "User",
        back_populates="workspace_members"
    )