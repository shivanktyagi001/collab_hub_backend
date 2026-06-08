from sqlalchemy.orm import Session
from models.users import User
from schemas.workspace import WorkspaceCreate,WorkspaceUpdate
from models.workspace import Workspace
from models.workspace_member import WorkspaceMember,WorkspaceRole




def create_workspace(db:Session,current_user:User,workspace_data:WorkspaceCreate):
    workspace = Workspace(
        name= workspace_data.name,
        desc = workspace_data.desc,
        owner_id=current_user.id
    )
    if not workspace:
        raise ValueError("Invalid Details")
    db.add(workspace)
    db.flush()
    member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=current_user.id,
        role = WorkspaceRole.OWNER
    )
    db.add(member)
    db.commit()
    db.refresh(workspace)
    return workspace

def get_my_workspace(db: Session, curr_user: User, limit: int = 10, offset: int = 0):
    myWorkspaces = db.query(Workspace).join(WorkspaceMember).filter(
        WorkspaceMember.user_id == curr_user.id
    ).limit(limit).offset(offset).all()
    if not myWorkspaces:
        raise ValueError("No Workspace found")
    return myWorkspaces

def get_workspace_by_id(db:Session,curr_user:User,workspaceId:int):
    workspaces = (db.query(Workspace).join(WorkspaceMember).filter(
        Workspace.id == workspaceId,
        WorkspaceMember.user_id == curr_user.id
    ).first())
    if not workspaces :
        raise ValueError("Workspace is not found or access denied")
    return workspaces

def update_workspace(db:Session,curr_user:User,workspace_id:int,workspace_data:WorkspaceUpdate):
    membership = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == curr_user.id
    ).first()

    if not membership:
        raise ValueError("Access denied")
    if  membership.role not in[
        WorkspaceRole.OWNER,
        WorkspaceRole.ADMIN
    ]:
        raise ValueError("only Admin and owner can edit the workspace")
    updated_workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not updated_workspace:
        raise ValueError("Workspace not found")

    if workspace_data.name:
        updated_workspace.name = workspace_data.name
    if workspace_data.desc:
        updated_workspace.desc = workspace_data.desc

    db.commit()
    db.refresh(updated_workspace)
    return updated_workspace

def delete_workspace(db:Session,workspace_id:int):
    workspace= db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace :
        raise ValueError("WorkSpace not found")
    db.delete(workspace)
    db.commit()
    return {
        "message":"Workspace deleted"
    }
