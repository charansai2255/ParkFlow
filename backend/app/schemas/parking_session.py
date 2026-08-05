from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ParkingSessionResponse(BaseModel):
    id: int

    reservation_id: int

    check_in_time: datetime

    check_out_time: datetime | None

    duration_minutes: int | None

    amount: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2, json_schema_extra={"example": "0.00"})

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )