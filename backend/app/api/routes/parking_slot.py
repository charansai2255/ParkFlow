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

from app.schemas.parking_slot import (
    ParkingSlotCreate,
    ParkingSlotResponse,
    ParkingSlotUpdate,
)

router = APIRouter(
    tags=["Parking Slots"],
)

@router.post(
    "/parking-floors/{floor_id}/slots",
    response_model=ParkingSlotResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_slot(
    floor_id: int,
    slot_data: ParkingSlotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    from app.services.parking_slot import (
        ParkingFloorNotFound,
        ParkingSlotAlreadyExists,
        add_slot,
    )

    try:
        return add_slot(db=db, floor_id=floor_id, slot_data=slot_data)
    except ParkingFloorNotFound:
        raise HTTPException(status_code=404, detail="Parking floor not found.")
    except ParkingSlotAlreadyExists:
        raise HTTPException(status_code=409, detail="Parking slot already exists.")

@router.get(
    "/parking-floors/{floor_id}/slots",
    response_model=list[ParkingSlotResponse],
)
def get_slots(
    floor_id: int,
    db: Session = Depends(get_db),
):
    from app.services.parking_slot import list_slots

    return list_slots(db=db, floor_id=floor_id)

@router.get(
    "/parking-slots/{slot_id}",
    response_model=ParkingSlotResponse,
)
def get_slot(
    slot_id: int,
    db: Session = Depends(get_db),
):
    from app.services.parking_slot import (
        ParkingSlotNotFound,
        get_slot_details,
    )

    try:
        return get_slot_details(db=db, slot_id=slot_id)
    except ParkingSlotNotFound:
        raise HTTPException(status_code=404, detail="Parking slot not found.")

@router.patch(
    "/parking-slots/{slot_id}",
    response_model=ParkingSlotResponse,
)
def update_slot(
    slot_id: int,
    slot_data: ParkingSlotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    from app.services.parking_slot import (
        ParkingSlotAlreadyExists,
        ParkingSlotNotFound,
        update_parking_slot,
    )

    try:
        return update_parking_slot(db=db, slot_id=slot_id, slot_data=slot_data)
    except ParkingSlotNotFound:
        raise HTTPException(status_code=404, detail="Parking slot not found.")
    except ParkingSlotAlreadyExists:
        raise HTTPException(status_code=409, detail="Parking slot already exists.")

@router.patch(
    "/parking-slots/{slot_id}/activate",
    response_model=ParkingSlotResponse,
)
def activate_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    from app.services.parking_slot import (
        ParkingSlotNotFound,
        activate_parking_slot,
    )

    try:
        return activate_parking_slot(db=db, slot_id=slot_id)
    except ParkingSlotNotFound:
        raise HTTPException(status_code=404, detail="Parking slot not found.")

@router.patch(
    "/parking-slots/{slot_id}/deactivate",
    response_model=ParkingSlotResponse,
)
def deactivate_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    from app.services.parking_slot import (
        ParkingSlotNotFound,
        deactivate_parking_slot,
    )

    try:
        return deactivate_parking_slot(db=db, slot_id=slot_id)
    except ParkingSlotNotFound:
        raise HTTPException(status_code=404, detail="Parking slot not found.")

