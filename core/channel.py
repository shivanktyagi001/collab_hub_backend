from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import (
    get_db,
    get_current_user
)

from models.users import User
from models.channel import Channel
from models.workspace_member import (
    WorkspaceMember,
    WorkspaceRole
)


def require_channel_access(
    channel_id: int,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)
):
    channel = db.query(Channel).filter(
        Channel.id == channel_id
    ).first()

    if not channel:
        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    membership = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == channel.workspace_id,
        WorkspaceMember.user_id == curr_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Not a workspace member"
        )

    if (
        channel.is_private
        and membership.role
        not in [
            WorkspaceRole.OWNER,
            WorkspaceRole.ADMIN
        ]
    ):
        raise HTTPException(
            status_code=403,
            detail="Private channel access denied"
        )

    return channel