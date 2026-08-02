from sqlalchemy import select,true
from sqlalchemy.orm import Session

from app import db
from app.models.parking_location import ParkingLocation


def get_location_by_name(
    db: Session,
    name: str,
) -> ParkingLocation | None:
    statement = select(ParkingLocation).where(
        ParkingLocation.name == name
    )
    return db.scalar(statement)


def get_location_by_id(
    db: Session,
    location_id: int,
) -> ParkingLocation | None:
    statement = select(ParkingLocation).where(
        ParkingLocation.id == location_id
    )
    return db.scalar(statement)


def get_all_locations(
    db: Session,
) -> list[ParkingLocation]:
    statement = (
        select(ParkingLocation)
        .where(ParkingLocation.is_active.is_(True))
        .order_by(ParkingLocation.name)
    )
    return list(db.scalars(statement).all())


def create_location(
    db: Session,
    location: ParkingLocation,
) -> ParkingLocation:
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update_location(
    db: Session,
    location: ParkingLocation,
) -> ParkingLocation:
    db.commit()
    db.refresh(location)
    return location

def deactivate_location(
    db: Session,
    location: ParkingLocation,
) -> ParkingLocation:
    location.is_active = False

    db.commit()
    db.refresh(location)

    return location


def activate_location(
    db: Session,
    location: ParkingLocation,
) -> ParkingLocation:
    location.is_active = True

    db.commit()
    db.refresh(location)

    return location