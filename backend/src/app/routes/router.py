import logging
from fastapi import APIRouter

from app.routes.health import router as health_router
from app.routes.runners import router as runners_router
from app.routes.checkpoints import router as checkpoints_router
from app.routes.races import router as races_router
from app.routes.events import router as events_router


logger = logging.getLogger(__name__)

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(runners_router)
api_router.include_router(checkpoints_router)
api_router.include_router(races_router)
api_router.include_router(events_router)

logger.debug("API router initialized with all endpoints")
