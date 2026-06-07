from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database.dependency import get_db
from core.dependencies import (
    get_current_user
)

from core.workspace_dependencies import (
    require_workspace_admin,
    require_workspace_owner
)

from core.channel import (
    require_channel_access
)

from models.users import User

from schemas.channel import (
    CreateChannelRequest,
    UpdateChannelRequest,
    ChannelResponse
)

from services.channel_services import (
    create_channel,
    list_channels,
    get_channel_by_id,
    update_channel,
    delete_channel
)

router = APIRouter(
    prefix="/channels",
    tags=["channels"]
)

@router.post("/workspace/{workspace_id}",response_model=ChannelResponse)
def create_channel_route(
     workspace_id: int,
    request: CreateChannelRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership=Depends(require_workspace_admin)
):
    try:
        return create_channel(
            db,
            workspace_id,
            request,
            current_user
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get(
    "/workspace/{workspace_id}",
    response_model=list[ChannelResponse]
)
def list_channels_route(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return list_channels(
            db,
            workspace_id,
            current_user
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get(
    "/{channel_id}",
    response_model=ChannelResponse
)
def get_channel_route(
    channel=Depends(require_channel_access),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return channel
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.patch(
    "/{channel_id}",
    response_model=ChannelResponse
)
def update_channel_route(
    channel_id: int,
    request: UpdateChannelRequest,
    db: Session = Depends(get_db),
    membership=Depends(require_workspace_admin)
):
    try:
        return update_channel(
            db,
            channel_id,
            request
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete(
    "/{channel_id}"
)
def delete_channel_route(
    channel_id: int,
    db: Session = Depends(get_db),
    membership=Depends(require_workspace_owner)
):
    try:
        return delete_channel(
            db,
            channel_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )