from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.parking_floor import ParkingFloor


def get_floor_by_id(
    db: Session,
    floor_id: int,
) -> ParkingFloor | None:
    statement = select(ParkingFloor).where(
        ParkingFloor.id == floor_id
    )

    return db.scalar(statement)


def get_floor(
    db: Session,
    *,
    location_id: int,
    floor_number: int,
) -> ParkingFloor | None:
    statement = select(ParkingFloor).where(
        ParkingFloor.location_id == location_id,
        ParkingFloor.floor_number == floor_number,
    )

    return db.scalar(statement)


def get_location_floors(
    db: Session,
    location_id: int,
) -> list[ParkingFloor]:
    statement = (
        select(ParkingFloor)
        .where(
            ParkingFloor.location_id == location_id,
            ParkingFloor.is_active.is_(True),
        )
        .order_by(ParkingFloor.floor_number)
    )

    return list(
        db.scalars(statement).all()
    )


def create_floor(
    db: Session,
    floor: ParkingFloor,
):
    db.add(floor)
    db.commit()
    db.refresh(floor)

    return floor


def update_floor(
    db: Session,
    floor: ParkingFloor,
):
    db.commit()
    db.refresh(floor)

    return floor

def deactivate_floor(
    db: Session,
    floor: ParkingFloor,
) -> ParkingFloor:
    floor.is_active = False

    db.commit()
    db.refresh(floor)

    return floor


def activate_floor(
    db: Session,
    floor: ParkingFloor,
) -> ParkingFloor:
    floor.is_active = True

    db.commit()
    db.refresh(floor)

    return floor