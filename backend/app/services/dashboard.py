from sqlalchemy.orm import Session

from app.models.enums import (
    SlotStatus,
    ReservationStatus,
)

from app.repositories.dashboard import (
    count_completed_sessions,
    count_floors,
    count_locations,
    count_slots,
    count_slots_by_status,
    count_today_reservations,
    count_reservations_by_status,
)

from app.schemas.dashboard import (
    DashboardSummaryResponse,
    RevenueResponse,
    OccupancyResponse,
    ReservationDashboardResponse,
)
from app.repositories.dashboard import (
    get_total_revenue,
    get_average_revenue,
)

def get_dashboard_summary(
    db: Session,
) -> DashboardSummaryResponse:

    total_locations = count_locations(db)

    total_floors = count_floors(db)

    total_slots = count_slots(db)

    available_slots = count_slots_by_status(
        db,
        SlotStatus.AVAILABLE,
    )

    reserved_slots = count_slots_by_status(
        db,
        SlotStatus.RESERVED,
    )

    occupied_slots = count_slots_by_status(
        db,
        SlotStatus.OCCUPIED,
    )

    today_reservations = count_today_reservations(
        db
    )

    completed_sessions = count_completed_sessions(
        db
    )

    if total_slots == 0:
        occupancy_rate = 0.0
    else:
        occupancy_rate = round(
            (occupied_slots / total_slots) * 100,
            2,
        )

    return DashboardSummaryResponse(
        total_locations=total_locations,
        total_floors=total_floors,
        total_slots=total_slots,
        available_slots=available_slots,
        reserved_slots=reserved_slots,
        occupied_slots=occupied_slots,
        today_reservations=today_reservations,
        completed_sessions=completed_sessions,
        occupancy_rate=occupancy_rate,
    )


def get_revenue_dashboard(
    db: Session,
):
    return RevenueResponse(
        total_revenue=get_total_revenue(db),
        average_session_revenue=get_average_revenue(db),
        completed_sessions=count_completed_sessions(
            db
        ),
    )

def get_occupancy_dashboard(
    db: Session,
):
    total = count_slots(db)

    available = count_slots_by_status(
        db,
        SlotStatus.AVAILABLE,
    )

    reserved = count_slots_by_status(
        db,
        SlotStatus.RESERVED,
    )

    occupied = count_slots_by_status(
        db,
        SlotStatus.OCCUPIED,
    )

    occupancy = (
        0
        if total == 0
        else round(
            occupied * 100 / total,
            2,
        )
    )

    return OccupancyResponse(
        available=available,
        reserved=reserved,
        occupied=occupied,
        occupancy_rate=occupancy,
    )
    
def get_reservation_dashboard(
    db: Session,
):
    return ReservationDashboardResponse(
        confirmed=count_reservations_by_status(
            db,
            ReservationStatus.CONFIRMED,
        ),
        checked_in=count_reservations_by_status(
            db,
            ReservationStatus.CHECKED_IN,
        ),
        completed=count_reservations_by_status(
            db,
            ReservationStatus.COMPLETED,
        ),
        cancelled=count_reservations_by_status(
            db,
            ReservationStatus.CANCELLED,
        ),
    )