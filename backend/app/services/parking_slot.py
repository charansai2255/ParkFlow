from sqlalchemy.orm import Session

from app.models.parking_floor import ParkingFloor
from app.models.parking_slot import ParkingSlot

from app.repositories.parking_floor import get_floor_by_id
from app.repositories.parking_slot import (
    activate_slot,
    create_slot,
    deactivate_slot,
    get_floor_slots,
    get_slot,
    get_slot_by_id,
    update_slot,
)

from app.schemas.parking_slot import (
    ParkingSlotCreate,
    ParkingSlotUpdate,
)


class ParkingFloorNotFound(Exception):
    pass


class ParkingSlotAlreadyExists(Exception):
    pass


class ParkingSlotNotFound(Exception):
    pass


def add_slot(
    db: Session,
    *,
    floor_id: int,
    slot_data: ParkingSlotCreate,
):
    floor: ParkingFloor | None = get_floor_by_id(
        db,
        floor_id,
    )

    if floor is None:
        raise ParkingFloorNotFound()

    existing = get_slot(
        db,
        floor_id=floor_id,
        slot_number=slot_data.slot_number,
    )

    if existing:
        raise ParkingSlotAlreadyExists()

    slot = ParkingSlot(
        floor_id=floor_id,
        **slot_data.model_dump(),
    )

    return create_slot(
        db,
        slot,
    )


def list_slots(
    db: Session,
    floor_id: int,
):
    return get_floor_slots(
        db,
        floor_id,
    )


def get_slot_details(
    db: Session,
    slot_id: int,
):
    slot = get_slot_by_id(
        db,
        slot_id,
    )

    if slot is None:
        raise ParkingSlotNotFound()

    return slot


def update_parking_slot(
    db: Session,
    *,
    slot_id: int,
    slot_data: ParkingSlotUpdate,
):
    slot = get_slot_by_id(
        db,
        slot_id,
    )

    if slot is None:
        raise ParkingSlotNotFound()

    update_data = slot_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if (
        "slot_number" in update_data
        and update_data["slot_number"] != slot.slot_number
    ):
        existing = get_slot(
            db,
            floor_id=slot.floor_id,
            slot_number=update_data["slot_number"],
        )

        if existing:
            raise ParkingSlotAlreadyExists()

    for key, value in update_data.items():
        setattr(slot, key, value)

    return update_slot(
        db,
        slot,
    )


def activate_parking_slot(
    db: Session,
    *,
    slot_id: int,
):
    slot = get_slot_by_id(
        db,
        slot_id,
    )

    if slot is None:
        raise ParkingSlotNotFound()

    if slot.is_active:
        return slot

    return activate_slot(
        db,
        slot,
    )


def deactivate_parking_slot(
    db: Session,
    *,
    slot_id: int,
):
    slot = get_slot_by_id(
        db,
        slot_id,
    )

    if slot is None:
        raise ParkingSlotNotFound()

    if not slot.is_active:
        return slot

    return deactivate_slot(
        db,
        slot,
    )