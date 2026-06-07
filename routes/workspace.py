from fastapi import APIRouter,Depends,HTTPException
from schemas.workspace import WorkspaceResponse,WorkspaceCreate,WorkspaceUpdate
from services.workspace_service import create_workspace,get_my_workspace,get_workspace_by_id,update_workspace,delete_workspace
from sqlalchemy.orm import Session
from typing import List
from core.dependencies import get_current_user,get_db
from core.workspace_dependencies import require_workspace_member
from models.users import User
from models.workspace_member import WorkspaceRole,WorkspaceMember
from schemas.workspace_member import InviteMemberRequest,WorkspaceMemberResponse,WorkspaceMemberCreateResponse
from services.workspace_member import invite_member,list_workspace_members,remove_members

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)

@router.post("/create_workspace",response_model=WorkspaceResponse)
def create_workspace_route(workspcae_data:WorkspaceCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    try:
        return create_workspace(db,current_user,workspcae_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/",response_model=List[WorkspaceResponse])
def get_my_workspace_route(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    try:
        return get_my_workspace(db,current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/{workspace_id}",response_model=WorkspaceResponse)
def get_workspace_by_id_route(worspace_id:int,db:Session=Depends(get_db),current_user:User= Depends(get_current_user)):
    try:
        return get_workspace_by_id(db,current_user,worspace_id)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.patch("/update/{workspace_id}",response_model=WorkspaceResponse)
def update_worspace(workspace_id:int,workspace_data:WorkspaceUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    try:
        return update_workspace(db,current_user,workspace_id,workspace_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.delete("/delete/{workspace_id}")
def delete_workspace_route(workspace_id:int,db:Session=Depends(get_db),membership:WorkspaceMember=Depends(require_workspace_member)):
    if  membership.role != WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only the owner can delete the workspace"
        )
    try:
        return delete_workspace(db,workspace_id)
    except ValueError as e:
        raise HTTPException(
                status_code=404,
                detail=str(e)
            )


@router.post("/{workspace_id}/invite",response_model=WorkspaceMemberCreateResponse)
def invite_member_route(workspace_id:int,request:InviteMemberRequest,db:Session=Depends(get_db),membership:WorkspaceMember=Depends(require_workspace_member)):
    if membership.role not in [
    WorkspaceRole.ADMIN,
    WorkspaceRole.OWNER
]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    try:
        return invite_member(db,workspace_id,request)
    except ValueError as e:
        raise HTTPException(
                status_code=404,
                detail=str(e)
            )
    


@router.get("/{workspace_id}/members",response_model=List[WorkspaceMemberResponse])
def list_workspace_members_route(workspace_id:int,db:Session=Depends(get_db),membership=Depends(require_workspace_member)):
    return list_workspace_members(db,workspace_id)

@router.delete("/{workspace_id}/members/{user_id}")
def remove_member_route(
    workspace_id:int,
    user_id:int,
    db:Session=Depends(get_db),
    membership :WorkspaceMember=Depends(require_workspace_member),

):
    if  membership.role == WorkspaceRole.MEMBER:
        raise HTTPException(
            status_code=403,
            detail="Members cannot remove users"
        )
    try:
        return remove_members(db,workspace_id,user_id,membership)
    except ValueError as e:
        raise HTTPException(
                status_code=404,
                detail=str(e)
            )
