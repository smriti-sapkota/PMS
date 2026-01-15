from fastapi import FastAPI
from .router import auth , users , rooms

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rooms.router)

#i m bored\.