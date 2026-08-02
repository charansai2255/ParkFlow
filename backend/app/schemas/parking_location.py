from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ParkingLocationCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=150,
    )

    address: str = Field(
        min_length=5,
    )

    city: str = Field(
        min_length=2,
        max_length=100,
    )

    state: str = Field(
        min_length=2,
        max_length=100,
    )

    country: str = Field(
        min_length=2,
        max_length=100,
    )

    postal_code: str = Field(
        min_length=3,
        max_length=20,
    )

    latitude: float

    longitude: float

    opening_time: time

    closing_time: time

    @field_validator(
        "name",
        "city",
        "state",
        "country",
        mode="before",
    )
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("closing_time")
    @classmethod
    def validate_closing_time(
        cls,
        value: time,
        info,
    ) -> time:
        opening_time = info.data.get("opening_time")

        if opening_time and value <= opening_time:
            raise ValueError(
                "Closing time must be later than opening time."
            )

        return value


class ParkingLocationUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=150,
    )

    address: str | None = None

    city: str | None = None

    state: str | None = None

    country: str | None = None

    postal_code: str | None = None

    latitude: float | None = None

    longitude: float | None = None

    opening_time: time | None = None

    closing_time: time | None = None

    is_active: bool | None = None


class ParkingLocationResponse(BaseModel):
    id: int

    name: str

    address: str

    city: str

    state: str

    country: str

    postal_code: str

    latitude: float

    longitude: float

    opening_time: time

    closing_time: time

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )