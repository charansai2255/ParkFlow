from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from app.services.vehicle import (
    VehicleAlreadyExistsError,
    VehicleNotFoundError,
    add_vehicle,
    list_user_vehicles,
    get_user_vehicle,
    update_user_vehicle,
    delete_user_vehicle
)
router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
)


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VehicleResponse:
    try:
        return add_vehicle(
            db,
            user_id=current_user.id,
            vehicle_data=vehicle_data,
        )

    except VehicleAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vehicle is already registered.",
        )
        
@router.get(
    "",
    response_model=list[VehicleResponse],
)
def list_vehicles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[VehicleResponse]:
    return list_user_vehicles(
        db,
        current_user.id,
    )
    
@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VehicleResponse:
    try:
        return get_user_vehicle(
            db,
            vehicle_id=vehicle_id,
            user_id=current_user.id,
        )

    except VehicleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found.",
        )
        
@router.patch(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def update_vehicle_endpoint(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VehicleResponse:
    try:
        return update_user_vehicle(
            db,
            vehicle_id=vehicle_id,
            user_id=current_user.id,
            vehicle_data=vehicle_data,
        )

    except VehicleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found.",
        )

    except VehicleAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vehicle is already registered.",
        )
        
@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vehicle_endpoint(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    try:
        delete_user_vehicle(
            db,
            vehicle_id=vehicle_id,
            user_id=current_user.id,
        )

    except VehicleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found.",
        )