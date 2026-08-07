from app.websocket.manager import manager


async def broadcast_slot_status(
    *,
    slot_id: int,
    status: str,
):
    await manager.broadcast(
        {
            "event": "slot_status_changed",
            "slot_id": slot_id,
            "status": status,
        }
    )


async def broadcast_reservation_created(
    *,
    reservation_id: int,
    slot_id: int,
):
    await manager.broadcast(
        {
            "event": "reservation_created",
            "reservation_id": reservation_id,
            "slot_id": slot_id,
        }
    )


async def broadcast_reservation_cancelled(
    *,
    reservation_id: int,
    slot_id: int,
):
    await manager.broadcast(
        {
            "event": "reservation_cancelled",
            "reservation_id": reservation_id,
            "slot_id": slot_id,
        }
    )


async def broadcast_check_in(
    *,
    reservation_id: int,
    slot_id: int,
):
    await manager.broadcast(
        {
            "event": "vehicle_checked_in",
            "reservation_id": reservation_id,
            "slot_id": slot_id,
        }
    )


async def broadcast_check_out(
    *,
    reservation_id: int,
    slot_id: int,
):
    await manager.broadcast(
        {
            "event": "vehicle_checked_out",
            "reservation_id": reservation_id,
            "slot_id": slot_id,
        }
    )