from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status

from app.schemas.message import Message
from app.services.connection_manager import manager

router = APIRouter()

@router.websocket("/{room_name}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_name: str,
    username: str = Query(...),
    password: Optional[str] = Query(None),
):
    # verifica existência da sala
    if room_name not in manager.active_connections:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    # verifica senha se privada
    if not manager.authenticate(room_name, password):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    # checa username único
    if manager.is_username_taken(room_name, username):
        await websocket.accept()
        await websocket.send_json({
            "username": "system",
            "message": f"Usuário '{username}' já existe na sala.",
            "timestamp": datetime.utcnow().isoformat()
        })
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # conecta o usuário
    await manager.connect(room_name, username, websocket)
    # notifica entrada
    await manager.broadcast(room_name, {
        "username": "system",
        "message": f"{username} entrou na sala.",
        "timestamp": datetime.utcnow().isoformat()
    })

    try:
        while True:
            data = await websocket.receive_text()
            # monta a mensagem com timestamp serializável
            msg = Message(username=username, message=data, timestamp=datetime.utcnow())
            msg_dict = msg.dict()
            msg_dict["timestamp"] = msg_dict["timestamp"].isoformat()
            await manager.broadcast(room_name, msg_dict)
    except WebSocketDisconnect:
        manager.disconnect(room_name, username)
        await manager.broadcast(room_name, {
            "username": "system",
            "message": f"{username} saiu da sala.",
            "timestamp": datetime.utcnow().isoformat()
        })
