from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.websocket.manager import manager

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/parking")
async def parking_websocket(
    websocket: WebSocket,
):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
        
@router.post("/test-broadcast")
async def test_broadcast():
    await manager.broadcast(
        {
            "event": "test",
            "message": "Hello from ParkFlow!"
        }
    )

    return {
        "message": "Broadcast sent"
    }