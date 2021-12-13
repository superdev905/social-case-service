from datetime import datetime
from typing import List, Optional
from fastapi import status, Request, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import or_
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.database.main import get_database
from ...middlewares.auth import JWTBearer
from ...helpers.fetch_data import fetch_parameter_data, fetch_users_service, get_business_data, get_employee_data
from ...helpers.schema import SuccessResponse
from .model import SocialCase, SocialCaseDerivation, SocialCaseClose
from .schema import ClosingCreate, ClosingItem, DerivationCreate, DerivationItem, SocialCaseCreate, SocialCaseDetails, SocialCaseItem, SocialCaseSimple
from .services import create_professionals

router = APIRouter(prefix="/social-cases",
                   tags=["Casos sociales"],
                   dependencies=[Depends(JWTBearer())])


@router.get("", response_model=Page[SocialCaseItem])
def get_all(business_id: int = Query(None, alias="businessId"),
            start_date: Optional[datetime] = Query(None, alias="startDate"),
            end_date: Optional[datetime] = Query(None, alias="endDate"),
            zone: str = None,
            state: str = None,
            professional_id: int = Query(None, alias="professionalId"),
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


@router.get("/collect", response_model=List[SocialCaseSimple])
def get_all_simple(db: Session = Depends(get_database)):
    return db.query(SocialCase).filter(SocialCase.is_active == True).order_by(SocialCase.created_at).all()


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


@router.get("/{id}", response_model=SocialCaseDetails)
def get_one(req: Request,
            id: int,
            db: Session = Depends(get_database)):
    """
    Retorna los detalles de un caso social
    ---
    - **id**: id
    """
    social_case = db.query(SocialCase).filter(
        SocialCase.id == id).first()

    if not social_case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe una tarea con este id: %s".format(id))

    business = get_business_data(req, social_case.business_id)
    employee = get_employee_data(req, social_case.employee_id)
    area = fetch_parameter_data(req, "areas", social_case.area_id)
    professional = fetch_users_service(req,  social_case.professional_id)

    return {**social_case.__dict__,
            "business": business,
            "employee": employee,
            "area": area,
            "professional": professional}


@router.post("/{id}/derivation", response_model=DerivationItem)
def create_derivation(req: Request,
                      id: int,
                      body: DerivationCreate,
                      db: Session = Depends(get_database)):
    """
    Crea una derivación para un casos social
    ---
    - **id**: id
    """
    social_case = db.query(SocialCase).filter(
        SocialCase.id == id).first()

    if not social_case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe una tarea con este id: %s".format(id))

    user_id = req.user_id
    professionals = body.assigned_professionals
    new_derivation = jsonable_encoder(body, by_alias=False)

    del new_derivation["assigned_professionals"]
    new_derivation["created_by"] = user_id

    db_derivation = SocialCaseDerivation(**new_derivation)

    db.add(db_derivation)
    db.commit()
    db.refresh(db_derivation)

    create_professionals(db, professionals, db_derivation.id,  user_id)

    social_case.derivation_id = db_derivation.id
    social_case.state = "ASIGNADO"

    db.add(social_case)
    db.commit()
    db.refresh(social_case)

    return db_derivation


@router.get("/{id}/derivation/{derivation_id}", response_model=DerivationItem)
def get_derivation(req: Request,
                   id: int,
                   derivation_id: int,
                   db: Session = Depends(get_database)):
    """
    Retorna detalles de la derivación de un casos social
    ---
    - **id**: id
    """
    social_case = db.query(SocialCase).filter(
        SocialCase.id == id).first()

    if not social_case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un caso social con este id: %s" % format(id))

    derivation = db.query(SocialCaseDerivation).filter(
        SocialCaseDerivation.id == derivation_id).first()

    if not derivation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe una derivación con este id: %s" % format(derivation_id))

    return derivation


@router.post("/{id}/close", response_model=ClosingItem)
def close_case(req: Request,
               id: int,
               body: ClosingCreate,
               db: Session = Depends(get_database)):
    """
    Cierra un caso social
    ---
    - **id**: id
    """
    social_case = db.query(SocialCase).filter(
        SocialCase.id == id).first()

    if not social_case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un caso social con este id: %s".format(id))

    user_id = req.user_id

    status = jsonable_encoder(body, by_alias=False)
    status["created_by"] = user_id

    db_status = SocialCaseClose(**status)

    db.add(db_status)
    db.commit()
    db.refresh(db_status)

    social_case.closing_id = db_status.id
    social_case.state = "CERRADO"

    db.add(social_case)
    db.commit()
    db.refresh(social_case)

    return db_status
