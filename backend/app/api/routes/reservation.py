from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.dependencies import get_db

from app.models.user import User

from app.schemas.reservation import (
    ReservationCreate,
    ReservationResponse,
    ReservationUpdate,
)

from app.services.reservation import (
    ReservationNotFound,
    SlotUnavailable,
    VehicleNotFound,
    add_reservation,
    cancel_reservation,
    get_reservation,
    list_my_reservations,
    update_reservation_details,
)

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"],
)

@router.post(
    "",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reservation(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return add_reservation(
            db=db,
            user_id=current_user.id,
            reservation_data=reservation_data,
        )

    except VehicleNotFound:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found.",
        )

    except SlotUnavailable:
        raise HTTPException(
            status_code=409,
            detail="Parking slot is unavailable.",
        )
        
@router.get(
    "",
    response_model=list[ReservationResponse],
)
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_my_reservations(
        db=db,
        user_id=current_user.id,
    )
    
    
@router.get(
    "/{reservation_id}",
    response_model=ReservationResponse,
)
def get_reservation_by_id(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_reservation(
            db=db,
            reservation_id=reservation_id,
            user_id=current_user.id,
        )

    except ReservationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found.",
        )
        
        
@router.patch(
    "/{reservation_id}",
    response_model=ReservationResponse,
)
def update_reservation(
    reservation_id: int,
    reservation_data: ReservationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_reservation_details(
            db=db,
            reservation_id=reservation_id,
            user_id=current_user.id,
            reservation_data=reservation_data,
        )

    except ReservationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found.",
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
        
        
@router.patch(
    "/{reservation_id}/cancel",
    response_model=ReservationResponse,
)
def cancel_user_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return cancel_reservation(
            db=db,
            reservation_id=reservation_id,
            user_id=current_user.id,
        )

    except ReservationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found.",
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
        
        
