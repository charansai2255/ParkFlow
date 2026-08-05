from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.db.dependencies import get_db
from app.models.user import User, UserRole

from app.schemas.parking_floor import (
    ParkingFloorCreate,
    ParkingFloorResponse,
    ParkingFloorUpdate,
)

from app.services.parking_floor import (
    ParkingFloorAlreadyExists,
    ParkingFloorNotFound,
    ParkingLocationNotFound,
    activate_parking_floor,
    add_floor,
    deactivate_parking_floor,
    get_floor_details,
    list_floors,
    update_parking_floor,
)

router = APIRouter(
    tags=["Parking Floors"],
)

@router.post(
    "/parking-locations/{location_id}/floors",
    response_model=ParkingFloorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_floor(
    location_id: int,
    floor_data: ParkingFloorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    try:
        return add_floor(
            db=db,
            location_id=location_id,
            floor_data=floor_data,
        )

    except ParkingLocationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking location not found.",
        )

    except ParkingFloorAlreadyExists:
        raise HTTPException(
            status_code=409,
            detail="Floor already exists.",
        )
        
@router.get(
    "/parking-locations/{location_id}/floors",
    response_model=list[ParkingFloorResponse],
)
def get_floors(
    location_id: int,
    db: Session = Depends(get_db),
):
    return list_floors(
        db=db,
        location_id=location_id,
    )
    
@router.get(
    "/parking-floors/{floor_id}",
    response_model=ParkingFloorResponse,
)
def get_floor(
    floor_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_floor_details(
            db=db,
            floor_id=floor_id,
        )

    except ParkingFloorNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking floor not found.",
        )
        
@router.patch(
    "/parking-floors/{floor_id}",
    response_model=ParkingFloorResponse,
)
def update_floor(
    floor_id: int,
    floor_data: ParkingFloorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    try:
        return update_parking_floor(
            db=db,
            floor_id=floor_id,
            floor_data=floor_data,
        )

    except ParkingFloorNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking floor not found.",
        )

    except ParkingFloorAlreadyExists:
        raise HTTPException(
            status_code=409,
            detail="Floor number already exists for this location.",
        )
        
@router.patch(
    "/parking-floors/{floor_id}/activate",
    response_model=ParkingFloorResponse,
)
def activate_floor(
    floor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    try:
        return activate_parking_floor(
            db=db,
            floor_id=floor_id,
        )

    except ParkingFloorNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking floor not found.",
        )
        
@router.patch(
    "/parking-floors/{floor_id}/deactivate",
    response_model=ParkingFloorResponse,
)
def deactivate_floor(
    floor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    try:
        return deactivate_parking_floor(
            db=db,
            floor_id=floor_id,
        )

    except ParkingFloorNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking floor not found.",
        )
        
