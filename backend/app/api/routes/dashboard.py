from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.db.dependencies import get_db

from app.models.user import (
    User,
    UserRole,
)

from app.schemas.dashboard import (
    DashboardSummaryResponse,
    RevenueResponse,
    OccupancyResponse,
    ReservationDashboardResponse,
)

from app.services.dashboard import (
    get_dashboard_summary,
    get_revenue_dashboard,
    get_occupancy_dashboard,
    get_reservation_dashboard,
)
router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    return get_dashboard_summary(
        db=db,
    )


@router.get(
    "/revenue",
    response_model=RevenueResponse,
)
def revenue_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    return get_revenue_dashboard(
        db
    )


@router.get(
    "/occupancy",
    response_model=OccupancyResponse,
)
def occupancy_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    return get_occupancy_dashboard(
        db
    )
    
@router.get(
    "/reservations",
    response_model=ReservationDashboardResponse,
)
def reservation_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    return get_reservation_dashboard(
        db
    )