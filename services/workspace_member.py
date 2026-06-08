from models.users import User
from models.workspace_member import WorkspaceMember,WorkspaceRole
from sqlalchemy.orm import Session
from schemas.workspace_member import InviteMemberRequest
def invite_member(db:Session,workspace_id:int,request:InviteMemberRequest):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise ValueError("User not found")
    existing = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id==user.id
        ).first()
    if existing:
        raise ValueError ("Already a member")
    member = WorkspaceMember(
       workspace_id=workspace_id,
       user_id=user.id,
       role = request.role
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def list_workspace_members(
    db: Session,
    workspace_id: int,
    limit: int = 10,
    offset: int = 0
):
    members = (
        db.query(
            User.id.label("user_id"),
            User.username,
            User.email,
            WorkspaceMember.role,
            WorkspaceMember.joined_at,
            WorkspaceMember.workspace_id
        )
        .join(
            WorkspaceMember,
            WorkspaceMember.user_id == User.id
        )
        .filter(
            WorkspaceMember.workspace_id == workspace_id
        )
        .limit(limit)
        .offset(offset)
        .all()
    )

    return [
        {
            "user_id": member.user_id,
            "username": member.username,
            "email": member.email,
            "role": member.role,
            "joined_at": member.joined_at,
            "workspace_id": member.workspace_id,
        }
        for member in members
    ]


def remove_members(db:Session,workspace_id:int,target_id:int,actor_membership:WorkspaceMember):
    target = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == target_id
    ).first()
    if not target:
        raise ValueError ("Member not found")
    if (
        actor_membership.role == WorkspaceRole.ADMIN and
        target.role == WorkspaceRole.OWNER
    ):
        raise ValueError("Cannot remove owner")
    if target.role == WorkspaceRole.OWNER:
        raise ValueError("Cannot remove owner")
    db.delete(target)
    db.commit()
    return {
        "message":"Member removed"
    }
