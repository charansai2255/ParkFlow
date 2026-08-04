from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base
from app.models.enums import SlotStatus, SlotType

if TYPE_CHECKING:
    from app.models.parking_floor import ParkingFloor


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    __table_args__ = (
        UniqueConstraint(
            "floor_id",
            "slot_number",
            name="uq_floor_slot_number",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    floor_id: Mapped[int] = mapped_column(
        ForeignKey(
            "parking_floors.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    slot_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    slot_type: Mapped[SlotType] = mapped_column(
        Enum(SlotType),
        nullable=False,
        default=SlotType.STANDARD,
    )

    status: Mapped[SlotStatus] = mapped_column(
        Enum(SlotStatus),
        nullable=False,
        default=SlotStatus.AVAILABLE,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
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

    floor: Mapped["ParkingFloor"] = relationship(
        back_populates="slots",
    )