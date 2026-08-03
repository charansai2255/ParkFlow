from sqlalchemy.orm import Session

from app.models.parking_floor import ParkingFloor
from app.models.parking_location import ParkingLocation

from app.repositories.parking_floor import (
    create_floor,
    get_floor,
    get_floor_by_id,
    get_location_floors,
    update_floor,
    activate_floor,
    deactivate_floor
)

from app.repositories.parking_location import (
    get_location_by_id,
)

from app.schemas.parking_floor import (
    ParkingFloorCreate,
    ParkingFloorUpdate,
)


class ParkingFloorAlreadyExists(Exception):
    pass


class ParkingFloorNotFound(Exception):
    pass


class ParkingLocationNotFound(Exception):
    pass


def add_floor(
    db: Session,
    *,
    location_id: int,
    floor_data: ParkingFloorCreate,
) -> ParkingFloor:

    location: ParkingLocation | None = get_location_by_id(
        db,
        location_id,
    )

    if location is None:
        raise ParkingLocationNotFound()

    existing = get_floor(
        db,
        location_id=location_id,
        floor_number=floor_data.floor_number,
    )

    if existing:
        raise ParkingFloorAlreadyExists()

    floor = ParkingFloor(
        location_id=location_id,
        **floor_data.model_dump(),
    )

    return create_floor(
        db,
        floor,
    )


def list_floors(
    db: Session,
    location_id: int,
):
    return get_location_floors(
        db,
        location_id,
    )


def get_floor_details(
    db: Session,
    floor_id: int,
):
    floor = get_floor_by_id(
        db,
        floor_id,
    )

    if floor is None:
        raise ParkingFloorNotFound()

    return floor


def update_parking_floor(
    db: Session,
    *,
    floor_id: int,
    floor_data: ParkingFloorUpdate,
):
    floor = get_floor_by_id(
        db,
        floor_id,
    )

    if floor is None:
        raise ParkingFloorNotFound()

    update_data = floor_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if (
        "floor_number" in update_data
        and update_data["floor_number"] != floor.floor_number
    ):
        existing = get_floor(
            db,
            location_id=floor.location_id,
            floor_number=update_data["floor_number"],
        )

        if existing:
            raise ParkingFloorAlreadyExists()

    for key, value in update_data.items():
        setattr(floor, key, value)

    return update_floor(
        db,
        floor,
    )
    
def deactivate_parking_floor(
    db: Session,
    *,
    floor_id: int,
) -> ParkingFloor:

    floor = get_floor_by_id(
        db,
        floor_id,
    )

    if floor is None:
        raise ParkingFloorNotFound()

    if not floor.is_active:
        return floor

    return deactivate_floor(
        db,
        floor,
    )
    
def activate_parking_floor(
    db: Session,
    *,
    floor_id: int,
) -> ParkingFloor:

    floor = get_floor_by_id(
        db,
        floor_id,
    )

    if floor is None:
        raise ParkingFloorNotFound()

    if floor.is_active:
        return floor

    return activate_floor(
        db,
        floor,
    )