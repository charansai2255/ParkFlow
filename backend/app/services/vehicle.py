from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.repositories.vehicle import (
    create_vehicle,
    get_vehicle_by_number,
    get_vehicles_by_user,
    get_vehicle_by_id_and_user,
    update_vehicle,
    delete_vehicle
)
from app.schemas.vehicle import VehicleCreate
from app.schemas.vehicle import VehicleUpdate
class VehicleAlreadyExistsError(Exception):
    pass


class VehicleNotFoundError(Exception):
    pass


def add_vehicle(
    db: Session,
    *,
    user_id: int,
    vehicle_data: VehicleCreate,
) -> Vehicle:
    existing_vehicle = get_vehicle_by_number(
        db,
        vehicle_data.vehicle_number,
    )

    if existing_vehicle is not None:
        raise VehicleAlreadyExistsError

    try:
        return create_vehicle(
            db,
            user_id=user_id,
            vehicle_number=vehicle_data.vehicle_number,
            vehicle_type=vehicle_data.vehicle_type,
        )

    except IntegrityError as exc:
        db.rollback()
        raise VehicleAlreadyExistsError from exc


def list_user_vehicles(
    db: Session,
    user_id: int,
) -> list[Vehicle]:
    return get_vehicles_by_user(
        db,
        user_id,
    )
    

def get_user_vehicle(
    db: Session,
    *,
    vehicle_id: int,
    user_id: int,
) -> Vehicle:
    vehicle = get_vehicle_by_id_and_user(
        db,
        vehicle_id,
        user_id,
    )

    if vehicle is None:
        raise VehicleNotFoundError

    return vehicle

def update_user_vehicle(
    db: Session,
    *,
    vehicle_id: int,
    user_id: int,
    vehicle_data: VehicleUpdate,
) -> Vehicle:
    vehicle = get_user_vehicle(
        db,
        vehicle_id=vehicle_id,
        user_id=user_id,
    )

    if (
        vehicle_data.vehicle_number is not None
        and vehicle_data.vehicle_number != vehicle.vehicle_number
    ):
        existing_vehicle = get_vehicle_by_number(
            db,
            vehicle_data.vehicle_number,
        )

        if existing_vehicle is not None:
            raise VehicleAlreadyExistsError

    try:
        return update_vehicle(
            db,
            vehicle,
            vehicle_number=vehicle_data.vehicle_number,
            vehicle_type=vehicle_data.vehicle_type,
        )

    except IntegrityError as exc:
        db.rollback()
        raise VehicleAlreadyExistsError from exc
    
    
def delete_user_vehicle(
    db: Session,
    *,
    vehicle_id: int,
    user_id: int,
) -> None:
    vehicle = get_user_vehicle(
        db,
        vehicle_id=vehicle_id,
        user_id=user_id,
    )

    delete_vehicle(
        db,
        vehicle,
    )