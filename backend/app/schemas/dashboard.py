from pydantic import BaseModel
from decimal import Decimal

class DashboardSummaryResponse(BaseModel):
    total_locations: int
    total_floors: int
    total_slots: int

    available_slots: int
    reserved_slots: int
    occupied_slots: int

    today_reservations: int
    completed_sessions: int

    occupancy_rate: float


class RevenueResponse(BaseModel):
    total_revenue: Decimal

    average_session_revenue: Decimal

    completed_sessions: int

class OccupancyResponse(BaseModel):
    available: int
    reserved: int
    occupied: int
    occupancy_rate: float
    
class ReservationDashboardResponse(BaseModel):
    confirmed: int
    checked_in: int
    completed: int
    cancelled: int