from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.parking_session import ParkingSession


def create_parking_session(
    db: Session,
    parking_session: ParkingSession,
):
    db.add(parking_session)

    return parking_session


def get_session_by_id(
    db: Session,
    session_id: int,
):
    statement = select(ParkingSession).where(
        ParkingSession.id == session_id
    )

    return db.scalar(statement)


def get_session_by_reservation(
    db: Session,
    reservation_id: int,
):
    statement = select(ParkingSession).where(
        ParkingSession.reservation_id == reservation_id
    )

    return db.scalar(statement)


def update_parking_session(
    db: Session,
    parking_session: ParkingSession,
):
    db.commit()

    db.refresh(parking_session)

    return parking_session