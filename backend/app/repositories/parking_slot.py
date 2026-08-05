from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.parking_slot import ParkingSlot


def get_slot_by_id(
    db: Session,
    slot_id: int,
) -> ParkingSlot | None:
    statement = select(ParkingSlot).where(
        ParkingSlot.id == slot_id
    )

    return db.scalar(statement)


def get_slot(
    db: Session,
    *,
    floor_id: int,
    slot_number: str,
) -> ParkingSlot | None:
    statement = select(ParkingSlot).where(
        ParkingSlot.floor_id == floor_id,
        ParkingSlot.slot_number == slot_number,
    )

    return db.scalar(statement)


def get_floor_slots(
    db: Session,
    floor_id: int,
) -> list[ParkingSlot]:
    statement = (
        select(ParkingSlot)
        .where(
            ParkingSlot.floor_id == floor_id,
            ParkingSlot.is_active.is_(True),
        )
        .order_by(ParkingSlot.slot_number)
    )

    return list(db.scalars(statement).all())


def create_slot(
    db: Session,
    slot: ParkingSlot,
) -> ParkingSlot:
    db.add(slot)
    db.commit()
    db.refresh(slot)

    return slot


def update_slot(
    db: Session,
    slot: ParkingSlot,
) -> ParkingSlot:
    db.commit()
    db.refresh(slot)

    return slot


def activate_slot(
    db: Session,
    slot: ParkingSlot,
) -> ParkingSlot:
    slot.is_active = True

    db.commit()
    db.refresh(slot)

    return slot


def deactivate_slot(
    db: Session,
    slot: ParkingSlot,
) -> ParkingSlot:
    slot.is_active = False

    db.commit()
    db.refresh(slot)

    return slot


def get_slot_by_id_for_update(
    db: Session,
    slot_id: int,
):
    statement = (
        select(ParkingSlot)
        .where(
            ParkingSlot.id == slot_id
        )
        .with_for_update()
    )

    return db.scalar(statement)