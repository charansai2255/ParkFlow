from datetime import UTC, datetime
from decimal import Decimal
import math

from sqlalchemy.orm import Session

from app.models.enums import (
    ReservationStatus,
    SlotStatus,
)
from app.models.parking_session import ParkingSession

from app.repositories.parking_session import (
    create_parking_session,
    get_session_by_id,
    get_session_by_reservation,
    update_parking_session,
)
from app.repositories.reservation import (
    get_reservation_by_id,
)


class ParkingSessionNotFound(Exception):
    pass


class ReservationNotEligible(Exception):
    pass


class ParkingSessionAlreadyExists(Exception):
    pass


def check_in(
    db: Session,
    *,
    reservation_id: int,
):
    reservation = get_reservation_by_id(
        db,
        reservation_id,
    )

    if reservation is None:
        raise ReservationNotEligible()

    if reservation.status != ReservationStatus.CONFIRMED:
        raise ReservationNotEligible()

    existing_session = get_session_by_reservation(
        db,
        reservation_id,
    )

    if existing_session:
        raise ParkingSessionAlreadyExists()

    parking_session = ParkingSession(
        reservation_id=reservation.id,
        check_in_time=datetime.now(UTC),
    )

    try:
        create_parking_session(
            db,
            parking_session,
        )

        reservation.status = (
            ReservationStatus.CHECKED_IN
        )

        reservation.slot.status = (
            SlotStatus.OCCUPIED
        )

        db.commit()

        db.refresh(parking_session)

        return parking_session

    except Exception:
        db.rollback()
        raise


def check_out(
    db: Session,
    *,
    reservation_id: int,
):
    reservation = get_reservation_by_id(
        db,
        reservation_id,
    )

    if reservation is None:
        raise ReservationNotEligible()

    if reservation.status != ReservationStatus.CHECKED_IN:
        raise ReservationNotEligible()

    parking_session = get_session_by_reservation(
        db,
        reservation_id,
    )

    if parking_session is None:
        raise ParkingSessionNotFound()

    try:
        check_out_time = datetime.now(UTC)

        parking_session.check_out_time = check_out_time

        check_in_time = parking_session.check_in_time
        if check_in_time.tzinfo is None:
            check_in_time = check_in_time.replace(tzinfo=UTC)

        duration = (
            check_out_time
            - check_in_time
        )

        duration_minutes = int(
            duration.total_seconds() // 60
        )

        parking_session.duration_minutes = (
            duration_minutes
        )

        hours = math.ceil(
            duration_minutes / 60
        )

        parking_session.amount = Decimal(
            hours * 50
        )

        reservation.status = (
            ReservationStatus.COMPLETED
        )

        reservation.slot.status = (
            SlotStatus.AVAILABLE
        )

        db.commit()

        db.refresh(parking_session)

        return parking_session

    except Exception:
        db.rollback()
        raise


def get_parking_session(
    db: Session,
    *,
    session_id: int,
):
    parking_session = get_session_by_id(
        db,
        session_id,
    )

    if parking_session is None:
        raise ParkingSessionNotFound()

    return parking_session


def get_session_for_reservation(
    db: Session,
    *,
    reservation_id: int,
):
    parking_session = get_session_by_reservation(
        db,
        reservation_id,
    )

    if parking_session is None:
        raise ParkingSessionNotFound()

    return parking_session