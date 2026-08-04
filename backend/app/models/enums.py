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