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

from app.schemas.parking_session import (
    ParkingSessionResponse,
)

from app.services.parking_session import (
    ParkingSessionAlreadyExists,
    ParkingSessionNotFound,
    ReservationNotEligible,
    check_in,
    check_out,
    get_parking_session,
    get_session_for_reservation,
)

router = APIRouter(
    prefix="/parking-sessions",
    tags=["Parking Sessions"],
)

@router.post(
    "/reservations/{reservation_id}/check-in",
    response_model=ParkingSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def check_in_vehicle(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return check_in(
            db=db,
            reservation_id=reservation_id,
        )

    except ReservationNotEligible:
        raise HTTPException(
            status_code=400,
            detail="Reservation is not eligible for check-in.",
        )

    except ParkingSessionAlreadyExists:
        raise HTTPException(
            status_code=409,
            detail="Parking session already exists.",
        )
        
@router.post(
    "/reservations/{reservation_id}/check-out",
    response_model=ParkingSessionResponse,
)
def check_out_vehicle(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return check_out(
            db=db,
            reservation_id=reservation_id,
        )

    except ReservationNotEligible:
        raise HTTPException(
            status_code=400,
            detail="Reservation is not checked in.",
        )

    except ParkingSessionNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking session not found.",
        )
     
@router.get(
    "/{session_id}",
    response_model=ParkingSessionResponse,
)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return get_parking_session(
            db=db,
            session_id=session_id,
        )

    except ParkingSessionNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking session not found.",
        )
        
        
@router.get(
    "/reservation/{reservation_id}",
    response_model=ParkingSessionResponse,
)
def get_session_by_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return get_session_for_reservation(
            db=db,
            reservation_id=reservation_id,
        )

    except ParkingSessionNotFound:
        raise HTTPException(
            status_code=404,
            detail="Parking session not found.",
        )
        
           