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
            search: str = None,
            db: Session = Depends(get_database),
            pag_params: Params = Depends()):
    """
    Retorna los planes de intervención de casos sociales
    ---
    """
    filters = []
    search_filters = []

    if social_case_id:
        filters.append(InterventionPlan.social_case_id == social_case_id)
    if search:
        formatted_search = "{}%".format(search)
        search_filters.append(
            InterventionPlan.management_name.ilike(formatted_search))
        search_filters.append(
            InterventionPlan.professional_names.ilike(formatted_search))
    return paginate(db.query(InterventionPlan).filter(and_(or_(*filters, *search_filters), InterventionPlan.is_active == True)).order_by(InterventionPlan.created_at), pag_params)


@router.post("", response_model=PlanItem)
def create_case(req: Request,
                body: PlanCreate,
                db: Session = Depends(get_database)):
    """
    Crea una tarea del Plan de Intervención
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


@router.put("/{id}", response_model=PlanItem)
def update_task(id: int,
                body: PlanCreate,
                db: Session = Depends(get_database)):
    """
    Actualiza una tarea del Plan de intervención
    ---
    - **id**: Id de tarea
    - **body**: body
    """

    found_plan = db.query(InterventionPlan).filter(
        InterventionPlan.id == id).first()

    if not found_plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe una tarea con este id: %s".format(id))

    updated_plan = get_updated_obj(found_plan, body)

    db.add(updated_plan)
    db.commit()
    db.refresh(updated_plan)

    return updated_plan


@router.delete("/{id}", response_model=PlanItem)
def delete_task(id: int,
                db: Session = Depends(get_database)):
    """
    Elimina una tarea del Plan de Intervención
    ---
    - **id**: Id de tarea
    """

    found_plan = db.query(InterventionPlan).filter(
        InterventionPlan.id == id).first()

    if not found_plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe una tarea con este id: %s".format(id))

    found_plan.is_active = False

    db.add(found_plan)
    db.commit()
    db.refresh(found_plan)

    return found_plan
