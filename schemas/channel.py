from pydantic import BaseModel,Field
from datetime import datetime
class CreateChannelRequest(BaseModel):
    name :str = Field(
        min_length=1,
        max_length=100,
    )
    desc : str|None = Field(
        default=None,
        max_length=300
    )
    is_private:bool=False

class UpdateChannelRequest(BaseModel):
    name:str|None=None
    desc:str|None=None
    is_private:bool|None=None

class ChannelResponse(BaseModel):
    id:int
    workspace_id:int
    name:str
    desc:str|None
    is_private:bool
    created_by:int
    created_at:datetime
    updated_at:datetime
    model_config ={
        "from_attributes":True
    }