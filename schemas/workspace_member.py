from pydantic import BaseModel,EmailStr
from models.workspace_member import WorkspaceRole
from datetime import datetime
class InviteMemberRequest(BaseModel):
    email:EmailStr
    role:WorkspaceRole = WorkspaceRole.MEMBER

class WorkspaceMemberCreateResponse(BaseModel):
    id: int
    workspace_id: int
    user_id: int
    role: WorkspaceRole

class WorkspaceMemberResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: WorkspaceRole
    joined_at: datetime
    workspace_id:int

    model_config= {
        "from_attributes":True
    }