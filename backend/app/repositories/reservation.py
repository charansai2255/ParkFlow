from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import ReservationStatus
from app.models.reservation import Reservation


def create_reservation(
    db: Session,
    reservation: Reservation,
) -> Reservation:
    db.add(reservation)
    return reservation


def get_reservation_by_id(
    db: Session,
    reservation_id: int,
) -> Reservation | None:
    statement = select(Reservation).where(
        Reservation.id == reservation_id
    )

    return db.scalar(statement)


def get_user_reservations(
    db: Session,
    user_id: int,
):
    statement = (
        select(Reservation)
        .where(
            Reservation.user_id == user_id
        )
        .order_by(
            Reservation.created_at.desc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def get_active_reservation_for_slot(
    db: Session,
    slot_id: int,
):
    statement = select(Reservation).where(
        Reservation.slot_id == slot_id,
        Reservation.status.in_(
            [
                ReservationStatus.CONFIRMED,
                ReservationStatus.CHECKED_IN,
            ]
        ),
    )

    return db.scalar(statement)


def update_reservation(
    db: Session,
    reservation: Reservation,
):
    db.commit()
    db.refresh(reservation)

    return reservation