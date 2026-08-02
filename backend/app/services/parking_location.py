from sqlalchemy.orm import Session

from app.models.parking_location import ParkingLocation
from app.repositories.parking_location import (
    create_location,
    get_all_locations,
    get_location_by_id,
    get_location_by_name,
    deactivate_location,
    activate_location
)
from app.schemas.parking_location import (
    ParkingLocationCreate,
)
from app.schemas.parking_location import ParkingLocationUpdate
from app.repositories.parking_location import update_location

class ParkingLocationAlreadyExists(Exception):
    pass


class ParkingLocationNotFound(Exception):
    pass


def add_location(
    db: Session,
    location_data: ParkingLocationCreate,
) -> ParkingLocation:

    existing = get_location_by_name(
        db,
        location_data.name,
    )

    if existing:
        raise ParkingLocationAlreadyExists()

    location = ParkingLocation(
        **location_data.model_dump()
    )

    return create_location(
        db,
        location,
    )


def list_locations(
    db: Session,
):
    return get_all_locations(db)


def get_location(
    db: Session,
    location_id: int,
):
    location = get_location_by_id(
        db,
        location_id,
    )

    if location is None:
        raise ParkingLocationNotFound()

    return location


def update_parking_location(
    db: Session,
    location_id: int,
    location_data: ParkingLocationUpdate,
):
    location = get_location_by_id(
        db,
        location_id,
    )

    if location is None:
        raise ParkingLocationNotFound()

    if (
        location_data.name
        and location_data.name != location.name
    ):
        existing = get_location_by_name(
            db,
            location_data.name,
        )

        if existing:
            raise ParkingLocationAlreadyExists()

    update_data = location_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(location, key, value)

    return update_location(
        db,
        location,
    )
    
def deactivate_parking_location(
    db: Session,
    location_id: int,
):
    location = get_location_by_id(
        db,
        location_id,
    )

    if location is None:
        raise ParkingLocationNotFound()

    if not location.is_active:
        return location

    return deactivate_location(
        db,
        location,
    )


def activate_parking_location(
    db: Session,
    location_id: int,
):
    location = get_location_by_id(
        db,
        location_id,
    )

    if location is None:
        raise ParkingLocationNotFound()

    if location.is_active:
        return location

    return activate_location(
        db,
        location,
    )