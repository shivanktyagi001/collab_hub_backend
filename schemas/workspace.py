from pydantic import BaseModel
from datetime import datetime
class WorkspaceCreate(BaseModel):
    name :str
    desc :str |None = None

class WorkspaceResponse(BaseModel):
    id :int
    name :str
    desc:str|None = None
    created_at:datetime
    updated_at :datetime
    owner_id:int
    model_config = {
        "from_attributes": True
    }

class WorkspaceUpdate(BaseModel):
    name:str|None = None
    desc :str|None=None
