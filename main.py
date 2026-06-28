from fastapi import FastAPI,APIRouter
from database.session import Base,engine
import models.users,models.refresh_token,models.workspace,models.channel,models.workspace_member,models.message
from routes.auth import router as auth_router
from routes.workspace import router as worker_route
from routes.channel import router as channel_route
from routes.message import router as message_route
from websocket.chat_socket import router as websocket_route
from core.rabbitmq import connect_rabbitmq, close_rabbitmq
print(Base.metadata.tables.keys())
Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.on_event("startup")
async def startup_event():
	await connect_rabbitmq()


@app.on_event("shutdown")
async def shutdown_event():
	await close_rabbitmq()

app.include_router(auth_router)
app.include_router(worker_route)
app.include_router(channel_route)
app.include_router(message_route)
app.include_router(websocket_route)
