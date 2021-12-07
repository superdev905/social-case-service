from datetime import datetime
from typing import Optional
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
from .model import SocialCase
from .schema import SocialCaseCreate, SocialCaseItem

router = APIRouter(prefix="/social-cases",
                   tags=["Etapas del proceso"],
                   dependencies=[Depends(JWTBearer())])


@router.get("", response_model=Page[SocialCaseItem])
def get_all(business_id: int = Query(None, alias="businessId"),
            start_date: datetime = Query(None, alias="startDate"),
            end_date: datetime = Query(None, alias="endDate"),
            zone: str = None,
            state: str = None,
            professional_id: str = Query(None, alias="professionalId"),
            delegation: str = None,
            area_id: int = Query(None, alias="areaId"),
            db: Session = Depends(get_database),
            pag_params: Params = Depends()):
    """
    Retorna los casos sociales aplicando filtros
    ---
    """
    filters = []

    if(business_id):
        filters.append(SocialCase.business_id == business_id)
    if(professional_id):
        filters.append(SocialCase.professional_id == professional_id)
    if(delegation):
        filters.append(SocialCase.delegation.like(delegation))
    if(area_id):
        filters.append(SocialCase.area_id == area_id)
    if (zone):
        filters.append(SocialCase.zone.like(zone))
    if (state):
        filters.append(SocialCase.state.like(state))

    return paginate(db.query(SocialCase).filter(or_(*filters)).order_by(SocialCase.created_at), pag_params)


@router.post("", response_model=SocialCaseItem)
def create_case(req: Request,
                body: SocialCaseCreate,
                db: Session = Depends(get_database)):
    """
    Crea un nuevo caso social 
    ---
    - **body**: body
    """

    new_case = jsonable_encoder(body, by_alias=False)
    new_case["created_by"] = req.user_id
    new_case["state"] = "SOLICITADO"
    db_case = SocialCase(**new_case)

    db.add(db_case)
    db.commit()
    db.refresh(db_case)

    return db_case
