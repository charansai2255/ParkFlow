from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import SlotType, SlotStatus


class ParkingSlotCreate(BaseModel):
    slot_number: str = Field(
        min_length=2,
        max_length=20,
    )

    slot_type: SlotType = SlotType.STANDARD


class ParkingSlotUpdate(BaseModel):
    slot_number: str | None = Field(
        default=None,
        min_length=2,
        max_length=20,
    )

    slot_type: SlotType | None = None

    is_active: bool | None = None


class ParkingSlotResponse(BaseModel):
    id: int

    floor_id: int

    slot_number: str

    slot_type: SlotType

    status: SlotStatus

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )