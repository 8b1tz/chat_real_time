from fastapi import FastAPI

from app.routers import auth, chat, rooms

app = FastAPI()
