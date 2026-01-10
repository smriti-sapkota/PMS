from .config import settings
from sqlmodel import create_engine, Session , SQLModel
from typing import Annotated
from fastapi import Depends

DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionLocal = Annotated[Session , Depends(get_session)]  

def create_table_and_column():
    SQLModel.metadata.create_all(engine)

