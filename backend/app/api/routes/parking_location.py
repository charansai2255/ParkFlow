from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
    require_roles,
)
from app.db.dependencies import get_db
from app.models.user import (
    User,
    UserRole,
)
from app.schemas.parking_location import (
    ParkingLocationCreate,
    ParkingLocationResponse,
    ParkingLocationUpdate
    
)
from app.services.parking_location import (
    ParkingLocationAlreadyExists,
    ParkingLocationNotFound,
    add_location,
    get_location,
    list_locations,
    update_parking_location
)
from app.services.parking_location import (
    activate_parking_location,
    deactivate_parking_location
)

router = APIRouter(
    prefix="/parking-locations",
    tags=["Parking Locations"],
)


@router.get(
    "",
    response_model=list[ParkingLocationResponse],
)
def get_locations(
    db: Session = Depends(get_db),
):
    return list_locations(db)


@router.get(
    "/{location_id}",
    response_model=ParkingLocationResponse,
)
def get_location_by_id(
    location_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_location(
            db,
            location_id,
        )

    except ParkingLocationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking location not found.",
        )


@router.post(
    "",
    response_model=ParkingLocationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_location(
    location_data: ParkingLocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    try:
        return add_location(
            db,
            location_data,
        )

    except ParkingLocationAlreadyExists:
        raise HTTPException(
            status_code=409,
            detail="Parking location already exists.",
        )
        
@router.patch(
    "/{location_id}",
    response_model=ParkingLocationResponse,
)
def update_location_endpoint(
    location_id: int,
    location_data: ParkingLocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    try:
        return update_parking_location(
            db,
            location_id,
            location_data,
        )

    except ParkingLocationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking location not found.",
        )

    except ParkingLocationAlreadyExists:
        raise HTTPException(
            status_code=409,
            detail="Parking location already exists.",
        )
        
@router.patch(
    "/{location_id}/deactivate",
    response_model=ParkingLocationResponse,
)
def deactivate_location_endpoint(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    try:
        return deactivate_parking_location(
            db,
            location_id,
        )

    except ParkingLocationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking location not found.",
        )
        
@router.patch(
    "/{location_id}/activate",
    response_model=ParkingLocationResponse,
)
def activate_location_endpoint(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    try:
        return activate_parking_location(
            db,
            location_id,
        )

    except ParkingLocationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking location not found.",
        )