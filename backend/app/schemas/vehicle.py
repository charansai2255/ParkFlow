from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.vehicle import VehicleType


class VehicleCreate(BaseModel):
    vehicle_number: str = Field(
        min_length=4,
        max_length=20,
    )
    vehicle_type: VehicleType

    @field_validator("vehicle_number")
    @classmethod
    def normalize_vehicle_number(cls, value: str) -> str:
        return value.replace(" ", "").upper()


class VehicleResponse(BaseModel):
    id: int
    user_id: int
    vehicle_number: str
    vehicle_type: VehicleType
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class VehicleUpdate(BaseModel):
    vehicle_number: str | None = Field(
        default=None,
        min_length=4,
        max_length=20,
    )

    vehicle_type: VehicleType | None = None

    @field_validator("vehicle_number")
    @classmethod
    def normalize_vehicle_number(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return value.replace(" ", "").upper()