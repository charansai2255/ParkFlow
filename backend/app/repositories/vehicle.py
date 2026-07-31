from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle, VehicleType


def get_vehicle_by_number(
    db: Session,
    vehicle_number: str,
) -> Vehicle | None:
    statement = select(Vehicle).where(
        Vehicle.vehicle_number == vehicle_number
    )

    return db.scalar(statement)


def create_vehicle(
    db: Session,
    *,
    user_id: int,
    vehicle_number: str,
    vehicle_type: VehicleType,
) -> Vehicle:
    vehicle = Vehicle(
        user_id=user_id,
        vehicle_number=vehicle_number,
        vehicle_type=vehicle_type,
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle

def get_vehicles_by_user(
    db: Session,
    user_id: int,
) -> list[Vehicle]:
    statement = (
        select(Vehicle)
        .where(Vehicle.user_id == user_id)
        .order_by(Vehicle.created_at.desc())
    )

    return list(db.scalars(statement).all())


def get_vehicle_by_id_and_user(
    db: Session,
    vehicle_id: int,
    user_id: int,
) -> Vehicle | None:
    statement = select(Vehicle).where(
        Vehicle.id == vehicle_id,
        Vehicle.user_id == user_id,
    )

    return db.scalar(statement)

def update_vehicle(
    db: Session,
    vehicle: Vehicle,
    *,
    vehicle_number: str | None = None,
    vehicle_type: VehicleType | None = None,
) -> Vehicle:
    if vehicle_number is not None:
        vehicle.vehicle_number = vehicle_number

    if vehicle_type is not None:
        vehicle.vehicle_type = vehicle_type

    db.commit()
    db.refresh(vehicle)

    return vehicle

def delete_vehicle(
    db: Session,
    vehicle: Vehicle,
) -> None:
    db.delete(vehicle)
    db.commit()