from fastapi import APIRouter
from fastapi.param_functions import Depends
from .middlewares.auth import JWTBearer

from ..v1.modules.social_cases.routes import router as social_cases_routes
from ..v1.modules.intervention_plans.routes import router as plans_routes
from ..v1.modules.dashboard.routes import router as dashboard_routes

router = APIRouter(dependencies=[Depends(JWTBearer())])

router.include_router(social_cases_routes)
router.include_router(plans_routes)
router.include_router(dashboard_routes)
