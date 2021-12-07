from fastapi import APIRouter
from fastapi.param_functions import Depends
from .middlewares.auth import JWTBearer

from ..v1.modules.social_cases.routes import router as social_case_routes

router = APIRouter(dependencies=[Depends(JWTBearer())])

router.include_router(social_case_routes)
