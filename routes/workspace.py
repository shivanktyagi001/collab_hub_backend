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
from core.cache import cache_get_json,cache_set_json,cache_delete_pattern
router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)

@router.post("/create_workspace",response_model=WorkspaceResponse)
async def create_workspace_route(workspcae_data:WorkspaceCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    try:
        workspace= create_workspace(db,current_user,workspcae_data)
        await cache_delete_pattern(
            f"workspaces:list:{current_user.id}:*"
        )
        return workspace

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/",response_model=List[WorkspaceResponse])
async def get_my_workspace_route(
    limit: int = 10,
    offset: int = 0,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    try:
        if limit <= 0 or limit > 100:
            limit = 10
        if offset < 0:
            offset = 0
        
        cache_key = f"workspaces:list:{current_user.id}:{limit}:{offset}"
        cache = await cache_get_json(cache_key)
        if cache is not None:
            return cache
        
        workspace = get_my_workspace(
            db,current_user,limit,offset
        )
        payload = [
            WorkspaceResponse.model_validate(w).model_dump(mode="json")
            for w in workspace
        ]
        await cache_set_json(
            cache_key,payload,ttl_seconds=180,
        )
        return workspace
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/{workspace_id}",response_model=WorkspaceResponse)
async def get_workspace_by_id_route(workspace_id:int,db:Session=Depends(get_db),current_user:User= Depends(get_current_user)):
    try:
        cache_key = f"workspace:{current_user.id}:{workspace_id}"

        cached = await cache_get_json(cache_key)

        if cached is not None:
            return cached

        workspace = get_workspace_by_id(
            db,
            current_user,
            workspace_id,
        )

        payload = (
            WorkspaceResponse
            .model_validate(workspace)
            .model_dump(mode="json")
        )

        await cache_set_json(
            cache_key,
            payload,
            ttl_seconds=300,
        )

        return workspace
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.patch("/update/{workspace_id}",response_model=WorkspaceResponse)
async def update_worspace(workspace_id:int,workspace_data:WorkspaceUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    try:
        workspace= update_workspace(db,current_user,workspace_id,workspace_data)
        await cache_delete_pattern(
            f"workspace:{current_user.id}:{workspace_id}"
        )
        await cache_delete_pattern(
            f"workspaces:list:{current_user.id}:*"
        )
        return workspace
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.delete("/delete/{workspace_id}")
async def delete_workspace_route(workspace_id:int,db:Session=Depends(get_db),membership:WorkspaceMember=Depends(require_workspace_member)):
    if  membership.role != WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only the owner can delete the workspace"
        )
    try:
        result= delete_workspace(db,workspace_id)
        await cache_delete_pattern(
            f"workspace:{membership.user_id}:{workspace_id}"
        )

        await cache_delete_pattern(
            f"workspaces:list:{membership.user_id}:*"
        )
        return result
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
def list_workspace_members_route(
    workspace_id: int,
    limit: int = 10,
    offset: int = 0,
    db: Session=Depends(get_db),
    membership=Depends(require_workspace_member)
):
    if limit <= 0 or limit > 100:
        limit = 10
    if offset < 0:
        offset = 0
    
    return list_workspace_members(db, workspace_id, limit, offset)

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
