from sqlalchemy.orm import Session
from models.users import User
from fastapi import Depends ,HTTPException
from models import workspace_member,users
from core.dependencies import get_db,get_current_user
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


