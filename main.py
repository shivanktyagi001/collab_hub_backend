from fastapi import FastAPI,APIRouter
from database.session import Base,engine
import models.users,models.refresh_token,models.workspace,models.channel,models.workspace_member
from routes.auth import router as auth_router
from routes.workspace import router as worker_route
from routes.channel import router as channel_route
print(Base.metadata.tables.keys())
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth_router)
app.include_router(worker_route)
app.include_router(channel_route)

