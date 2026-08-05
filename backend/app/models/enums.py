from enum import Enum


class SlotType(str, Enum):
    STANDARD = "STANDARD"
    BIKE = "BIKE"
    EV = "EV"
    HANDICAP = "HANDICAP"


class SlotStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    HELD = "HELD"
    RESERVED = "RESERVED"
    OCCUPIED = "OCCUPIED"


class ReservationStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    CHECKED_IN = "CHECKED_IN"
    COMPLETED = "COMPLETED"
    NO_SHOW = "NO_SHOW"