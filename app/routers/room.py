from typing import List, Optional

from fastapi import APIRouter, HTTPException

from app.schemas.room import RoomCreate, RoomOut
from app.services.connection_manager import manager

router = APIRouter()

@router.post("/", response_model=RoomOut)
def create_room(room: RoomCreate):
    try:
        manager.create_room(room.name, room.password)
        return RoomOut(name=room.name, private=bool(room.password))
    except ValueError:
        raise HTTPException(status_code=400, detail="Sala já existe")

@router.get("/", response_model=List[RoomOut])
def list_rooms():
    return manager.list_rooms()
