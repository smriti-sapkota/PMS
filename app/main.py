from fastapi import FastAPI
from .router import auth , users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)