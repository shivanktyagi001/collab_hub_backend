from core.dependencies import get_current_user
from database.dependency import get_db
from schemas.channel import ChannelResponse,CreateChannelRequest,UpdateChannelRequest
from models.channel import Channel
from models.workspace import Workspace
from models.workspace_member import WorkspaceMember,WorkspaceRole
from models.users import User
from sqlalchemy.orm import Session
def create_channel(db:Session,workspace_id:int,request:CreateChannelRequest,curr_user:User):
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()
    if not workspace:
        raise ValueError("Workspace not found")
    existing_channel = db.query(Channel).filter(
        Channel.workspace_id == workspace_id,
        Channel.name == request.name
    ).first()
    if existing_channel:
        raise ValueError ("Channel already exists")
    channel = Channel(
        workspace_id=workspace_id,
        name=request.name,
        desc = request.desc,
        is_private=request.is_private,
        created_by= curr_user.id
    )
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel

def list_channels(db:Session,workspace_id:int,curr_user:User):
    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == curr_user.id
    ).first()
    if not member:
        raise ValueError("Not a workspace member")

    if member.role in [
        WorkspaceRole.ADMIN,
        WorkspaceRole.OWNER
    ]:
        return db.query(Channel).filter(
            Channel.workspace_id == workspace_id
        ).all()

    return db.query(Channel).filter(
        Channel.workspace_id == workspace_id,
        Channel.is_private == False
    ).all()

def get_channel_by_id(db:Session,channel_id:int,curr_user:User):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise ValueError("Channel not found")
    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == channel.workspace_id,
        WorkspaceMember.user_id == curr_user.id
    ).first()
    if not member:
        raise ValueError("Not a workspace member")
    if(channel.is_private and member.role not in [
        WorkspaceRole.ADMIN,
            WorkspaceRole.OWNER
    ]):
        raise ValueError("private Channel")
    
    return channel

def update_channel(
    db: Session,
    channel_id: int,
    request: UpdateChannelRequest
):

    channel = db.query(Channel).filter(
        Channel.id == channel_id
    ).first()

    if not channel:
        raise ValueError("Channel not found")

    if request.name is not None:
        channel.name = request.name

    if request.desc is not None:
        channel.desc = request.desc

    if request.is_private is not None:
        channel.is_private = request.is_private

    db.commit()
    db.refresh(channel)

    return channel

def delete_channel(
    db: Session,
    channel_id: int
):

    channel = db.query(Channel).filter(
        Channel.id == channel_id
    ).first()

    if not channel:
        raise ValueError("Channel not found")

    db.delete(channel)
    db.commit()

    return {
        "message": "Channel deleted successfully"
    }


