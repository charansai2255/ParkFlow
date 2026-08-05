from fastapi import APIRouter

from app.api.routes.auth import router as auth_router

from app.api.routes.vehicles import router as vehicles_router

from app.api.routes.parking_location import router as parking_location_router

from app.api.routes.parking_floor import router as parking_floor_router

from app.api.routes.parking_slot import router as parking_slot_router

from app.api.routes.reservation import  router as reservation_router

from app.api.routes.parking_session import (
    router as parking_session_router,
)

api_router = APIRouter(
    prefix="/api/v1",
)


api_router.include_router(auth_router)
api_router.include_router(vehicles_router)
api_router.include_router(parking_location_router)
api_router.include_router(parking_floor_router)
api_router.include_router(parking_slot_router)
api_router.include_router(reservation_router)
api_router.include_router(
    parking_session_router
)