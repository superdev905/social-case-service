from datetime import datetime
from typing import List, Optional
from fastapi import status, Request, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import and_, or_
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.database.main import get_database
from ...middlewares.auth import JWTBearer
from ...helpers.fetch_data import fetch_users_service, get_employee_data
from ...helpers.crud import get_updated_obj
from ...helpers.humanize_date import get_time_ago
from ...helpers.schema import SuccessResponse
from .model import InterventionPlan
from .schema import PlanCreate, PlanItem

router = APIRouter(prefix="/intervention-plans",
                   tags=["Planes de intervención"],
                   dependencies=[Depends(JWTBearer())])


@router.get("", response_model=Page[PlanItem])
def get_all(social_case_id: int = Query(None, alias="socialCaseId"),
            db: Session = Depends(get_database),
            pag_params: Params = Depends()):
    """
    Retorna los planes de intervención de casos sociales
    ---
    """
    filters = []

    return paginate(db.query(InterventionPlan).filter(or_(*filters)).order_by(InterventionPlan.created_at), pag_params)


@router.post("", response_model=PlanItem)
def create_case(req: Request,
                body: PlanCreate,
                db: Session = Depends(get_database)):
    """
    Crea un nuevo plan de intervención
    ---
    - **body**: body
    """

    new_plan = jsonable_encoder(body, by_alias=False)
    new_plan["created_by"] = req.user_id
    db_plan = InterventionPlan(**new_plan)

    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)

    return db_plan
