from sqlalchemy.orm import Session
from models.users import User
from fastapi import Depends ,HTTPException
from models import workspace_member,users
from core.dependencies import get_db,get_current_user
from models.workspace_member import WorkspaceRole
def require_workspace_member(workspace_id:int,db:Session=Depends(get_db),curr_user:User=Depends(get_current_user)):
    membership = db.query(workspace_member.WorkspaceMember).filter(
        workspace_member.WorkspaceMember.workspace_id == workspace_id,
        workspace_member.WorkspaceMember.user_id == curr_user.id
    ).first()
    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    return membership
def require_workspace_admin(workspace_id:int,db:Session=Depends(get_db),curr_user:User=Depends(get_current_user)):
    membership = db.query(workspace_member.WorkspaceMember).filter(
        workspace_member.WorkspaceMember.workspace_id == workspace_id,
        workspace_member.WorkspaceMember.user_id == curr_user.id
    ).first()
    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    if membership.role == WorkspaceRole.MEMBER:
        raise HTTPException(
            status_code=404,
            detail="Not allowed to perform this action"
        )
    return membership

def require_workspace_owner(workspace_id:int,db:Session=Depends(get_db),curr_user:User=Depends(get_current_user)):
    membership = db.query(workspace_member.WorkspaceMember).filter(
        workspace_member.WorkspaceMember.workspace_id == workspace_id,
        workspace_member.WorkspaceMember.user_id == curr_user.id
    ).first()
    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    if membership.role != WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only owner can perform this action"
        )
    return membership

