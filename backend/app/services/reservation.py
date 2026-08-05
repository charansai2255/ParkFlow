from sqlalchemy.orm import Session

from app.models.enums import (
    ReservationStatus,
    SlotStatus,
)
from app.models.reservation import Reservation

from app.repositories.parking_slot import (
    get_slot_by_id_for_update,
)
from app.repositories.reservation import (
    create_reservation,
    get_reservation_by_id,
    get_user_reservations,
    update_reservation,
)
from app.repositories.vehicle import (
    get_vehicle_by_id,
)

from app.schemas.reservation import (
    ReservationCreate,
    ReservationUpdate,
)


class ReservationNotFound(Exception):
    pass


class SlotUnavailable(Exception):
    pass


class VehicleNotFound(Exception):
    pass


def add_reservation(
    db: Session,
    *,
    user_id: int,
    reservation_data: ReservationCreate,
):
    vehicle = get_vehicle_by_id(
        db,
        reservation_data.vehicle_id,
    )

    if vehicle is None:
        raise VehicleNotFound()

    if vehicle.user_id != user_id:
        raise VehicleNotFound()

    slot = get_slot_by_id_for_update(
        db,
        reservation_data.slot_id,
    )

    if slot is None:
        raise SlotUnavailable()

    if not slot.is_active:
        raise SlotUnavailable()

    if slot.status != SlotStatus.AVAILABLE:
        raise SlotUnavailable()

    reservation = Reservation(
        user_id=user_id,
        vehicle_id=reservation_data.vehicle_id,
        slot_id=reservation_data.slot_id,
        start_time=reservation_data.start_time,
        end_time=reservation_data.end_time,
        status=ReservationStatus.CONFIRMED,
    )

    try:
        create_reservation(
            db,
            reservation,
        )

        slot.status = SlotStatus.RESERVED

        db.commit()

        db.refresh(reservation)

        return reservation

    except Exception:
        db.rollback()
        raise


def list_my_reservations(
    db: Session,
    *,
    user_id: int,
):
    return get_user_reservations(
        db,
        user_id,
    )


def get_reservation(
    db: Session,
    *,
    reservation_id: int,
    user_id: int,
):
    reservation = get_reservation_by_id(
        db,
        reservation_id,
    )

    if reservation is None:
        raise ReservationNotFound()

    if reservation.user_id != user_id:
        raise ReservationNotFound()

    return reservation


def update_reservation_details(
    db: Session,
    *,
    reservation_id: int,
    user_id: int,
    reservation_data: ReservationUpdate,
):
    reservation = get_reservation_by_id(
        db,
        reservation_id,
    )

    if reservation is None:
        raise ReservationNotFound()

    if reservation.user_id != user_id:
        raise ReservationNotFound()

    if reservation.status != ReservationStatus.CONFIRMED:
        raise ValueError(
            "Only confirmed reservations can be updated."
        )

    update_data = reservation_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    for key, value in update_data.items():
        setattr(
            reservation,
            key,
            value,
        )

    return update_reservation(
        db,
        reservation,
    )


def cancel_reservation(
    db: Session,
    *,
    reservation_id: int,
    user_id: int,
):
    reservation = get_reservation_by_id(
        db,
        reservation_id,
    )

    if reservation is None:
        raise ReservationNotFound()

    if reservation.user_id != user_id:
        raise ReservationNotFound()

    if reservation.status != ReservationStatus.CONFIRMED:
        raise ValueError(
            "Reservation cannot be cancelled."
        )

    reservation.status = ReservationStatus.CANCELLED

    reservation.slot.status = SlotStatus.AVAILABLE

    db.commit()

    db.refresh(reservation)

    return reservation