from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import (
    ReservationStatus,
    SlotStatus,
)
from app.models.parking_floor import ParkingFloor
from app.models.parking_location import ParkingLocation
from app.models.parking_session import ParkingSession
from app.models.parking_slot import ParkingSlot
from app.models.reservation import Reservation
from decimal import Decimal

def count_locations(
    db: Session,
) -> int:
    statement = select(
        func.count(ParkingLocation.id)
    )

    return db.scalar(statement) or 0


def count_floors(
    db: Session,
) -> int:
    statement = select(
        func.count(ParkingFloor.id)
    )

    return db.scalar(statement) or 0


def count_slots(
    db: Session,
) -> int:
    statement = select(
        func.count(ParkingSlot.id)
    )

    return db.scalar(statement) or 0


def count_slots_by_status(
    db: Session,
    slot_status: SlotStatus,
) -> int:
    statement = (
        select(
            func.count(ParkingSlot.id)
        )
        .where(
            ParkingSlot.status == slot_status
        )
    )

    return db.scalar(statement) or 0


def count_today_reservations(
    db: Session,
) -> int:
    now = datetime.now(UTC)

    start_of_day = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    end_of_day = start_of_day + timedelta(days=1)

    statement = (
        select(
            func.count(Reservation.id)
        )
        .where(
            Reservation.created_at >= start_of_day,
            Reservation.created_at < end_of_day,
        )
    )

    return db.scalar(statement) or 0


def count_completed_sessions(
    db: Session,
) -> int:
    statement = (
        select(
            func.count(Reservation.id)
        )
        .where(
            Reservation.status
            == ReservationStatus.COMPLETED
        )
    )

    return db.scalar(statement) or 0


def calculate_total_revenue(
    db: Session,
):
    statement = select(
        func.sum(ParkingSession.amount)
    )

    return db.scalar(statement) or 0


def get_total_revenue(
    db: Session,
):
    statement = select(
        func.sum(
            ParkingSession.amount
        )
    )

    return db.scalar(statement) or Decimal("0.00")


def get_average_revenue(
    db: Session,
):
    statement = select(
        func.avg(
            ParkingSession.amount
        )
    )

    return db.scalar(statement) or Decimal("0.00")

def count_reservations_by_status(
    db: Session,
    reservation_status: ReservationStatus,
):
    statement = (
        select(
            func.count(
                Reservation.id
            )
        )
        .where(
            Reservation.status
            == reservation_status
        )
    )

    return db.scalar(statement) or 0