from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base
from app.models.enums import ReservationStatus

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.vehicle import Vehicle
    from app.models.parking_slot import ParkingSlot


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey(
            "vehicles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    slot_id: Mapped[int] = mapped_column(
        ForeignKey(
            "parking_slots.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[ReservationStatus] = mapped_column(
        Enum(ReservationStatus),
        nullable=False,
        default=ReservationStatus.CONFIRMED,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="reservations",
    )

    vehicle: Mapped["Vehicle"] = relationship(
        back_populates="reservations",
    )

    slot: Mapped["ParkingSlot"] = relationship(
        back_populates="reservations",
    )