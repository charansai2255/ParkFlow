from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ParkingFloorCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    floor_number: int


class ParkingFloorUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    floor_number: int | None = None

    is_active: bool | None = None


class ParkingFloorResponse(BaseModel):
    id: int

    location_id: int

    name: str

    floor_number: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )