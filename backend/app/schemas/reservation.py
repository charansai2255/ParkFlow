from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ReservationStatus


class ReservationCreate(BaseModel):
    vehicle_id: int

    slot_id: int

    start_time: datetime

    end_time: datetime = Field(
        description="Reservation end time",
    )


class ReservationUpdate(BaseModel):
    start_time: datetime | None = None

    end_time: datetime | None = None


class ReservationResponse(BaseModel):
    id: int

    user_id: int

    vehicle_id: int

    slot_id: int

    start_time: datetime

    end_time: datetime

    status: ReservationStatus

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )