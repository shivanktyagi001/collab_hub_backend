from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./collab_hub.db")
engine  = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind=engine
)
class Base(DeclarativeBase):
    pass