from datetime import datetime
from os import getegid
from typing import List, Optional

from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import func
from fastapi import status, Request, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import and_, or_
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.settings import SERVICES
from app.database.main import get_database
from ...middlewares.auth import JWTBearer
from ...helpers.fetch_data import fetch_parameter_data, fetch_service, fetch_users_service, get_business_data, get_employee_data, get_assistance_information
from ...helpers.schema import SuccessResponse
from .model import SocialCase, SocialCaseDerivation, SocialCaseClose, AssignedProfessional
from .schema import ClosingCreate, ClosingItem, DerivationCreate, DerivationDetails, DerivationItem, SocialCaseBase, SocialCaseCreate, SocialCaseDetails, SocialCaseEmployee, SocialCaseItem, SocialCaseSimple, SocialCaseDerivationCreate, SocialCaseMail
from .services import create_professionals, get_assistance, patch_employee_status
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

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
            search: str = None,
            db: Session = Depends(get_database),
            pag_params: Params = Depends()):
    """
    Retorna los casos sociales aplicando filtros
    ---
    """
    filters = []
    extraFilters = []
    search_filters = []
    date_filters = []

    if(business_id):
        filters.append(SocialCase.business_id == business_id)
    if(professional_id):
        filters.append(SocialCase.professional_id == professional_id)
        extraFilters.append(SocialCase.assistance_derivation_id.contains([professional_id]))
    if(area_id):
        filters.append(SocialCase.area_id == area_id)
    if (start_date):
        date_filters.append(func.date(SocialCase.date) >= start_date)
    if (end_date):
        date_filters.append(func.date(SocialCase.date) <= end_date)
    if (state):
        filters.append(SocialCase.state == state)
    if(search):
        formatted_search = "{}%".format(search)
        search_filters.append(SocialCase.employee_rut.ilike(formatted_search))
        search_filters.append(
            SocialCase.employee_names.ilike(formatted_search))
        search_filters.append(
            SocialCase.business_name.ilike(formatted_search))

    return paginate(db.query(SocialCase).filter(or_(and_(*filters), *extraFilters, *search_filters, and_(*date_filters))).order_by(SocialCase.created_at.desc()), pag_params)


@router.get("/employee", response_model=Page[SocialCaseEmployee])
def get_employees_to_attend(req: Request, business_id: int = Query(None, alias="businessId"), user_id: int = Query(None, alias="userId"), construction_id: int = Query(None, alias="constructionId"),
                            db: Session = Depends(get_database),
                            pag_params: Params = Depends()):
    if business_id:
        business = get_business_data(req, business_id)

        if business["social_service"] == "SI":
            filters = []
            filters.append(SocialCase.business_id == business_id)
            filters.append(SocialCase.construction_id == construction_id)
            filters.append(SocialCase.state != "CERRADO")
            filters.append(SocialCase.is_active != False)

            result = paginate(db.query(SocialCase).filter(
                and_(*filters), and_(or_(SocialCase.created_by == user_id, SocialCase.assistance_derivation_id.contains([user_id])))).order_by(SocialCase.created_at.desc()), pag_params)
            docs = []
            for i in result.items:
                employee = get_employee_data(req, i.employee_id)
                docs.append({**i.__dict__, "employee": employee,
                            "motive": "Caso social"})
            result.items = docs
            return result
        else:
            return {"items": [], "page": 1, "size": 30, "total": 0}


@router.get("/collect/{id}", response_model=List[SocialCaseSimple])
def get_all_simple(id: int, db: Session = Depends(get_database)):
    return db.query(SocialCase).filter(and_(SocialCase.is_active == True, SocialCase.employee_id == id)).options(joinedload(SocialCase.intervention_plans)).order_by(SocialCase.created_at).all()


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

    patch_employee_status(req, body.employee_id, {"has_social_case": True})

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
    asistencia = get_assistance_information(req, social_case.assistance_id)

    return {**social_case.__dict__,
            "business": business,
            "employee": employee,
            "area": area,
            "tema": asistencia["topic"],
            "professional": professional,
            "observation": asistencia["observation"]}


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


@router.get("/{id}/derivation/{derivation_id}", response_model=DerivationDetails)
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

    professionals = []

    for i in derivation.assigned_professionals:
        contact = fetch_users_service(req, i.user_id)
        professionals.append(contact)

    return {**derivation.__dict__,
            "assigned_professionals": professionals}


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

    employee_cases = db.query(SocialCase).filter(and_(SocialCase.is_active == True,
                                                      SocialCase.employee_id == social_case.employee_id, SocialCase.state != "CERRADO")).first()

    patch_employee_status(req, social_case.employee_id, {
                          "has_social_case": bool(employee_cases)})

    return db_status

@router.put("/{id}", response_model=SocialCaseDerivationCreate)
def add_derivation_state_id(id: int, body: SocialCaseDerivationCreate, db: Session = Depends(get_database)):
    """
    Agrega el id del asistente a la que se le deriva
    ---
    - **id**: id
    """
    
    bodyRes = jsonable_encoder(body)
    social_case = db.query(SocialCase).filter(
        SocialCase.id == id
    ).first()

    setattr(social_case, 'assistance_derivation_id', bodyRes["assistanceDerivationId"])

    db.add(social_case)
    db.commit()
    db.refresh(social_case)

    result = jsonable_encoder(social_case)

    return{**result}

@router.put("/derivation/edit/{id}", response_model=DerivationDetails)
def update_derivation(req: Request, id: int, body: DerivationCreate, db: Session = Depends(get_database)):
    """
    Se actualiza una derivación
    ---
    - **id**: id del caso social
    """

    social_case = db.query(SocialCase).filter(SocialCase.id == id).first()
    edit_social_case = jsonable_encoder(social_case)

    social_case_service = db.query(SocialCaseDerivation).filter(SocialCaseDerivation.assistance_titular_id == edit_social_case["assistance_id"]).first()
    setattr(social_case_service, 'observations', body.observations)
    setattr(social_case_service, 'priority', body.priority)

    db.add(social_case_service)
    db.commit()
    db.refresh(social_case_service)

    edited_social_case_service = jsonable_encoder(social_case_service)
    db.query(AssignedProfessional).filter(AssignedProfessional.derivation_id == edited_social_case_service["id"]).delete()

    user_id = req.user_id
    professionals = body.assigned_professionals

    create_professionals(db, professionals, edited_social_case_service['id'],  user_id)

@router.post("/mail/social-case")
def send_social_case_mail(type: str, body: SocialCaseMail = None):
    #Variables:
    # type: Tipo de mensaje a enviar (CREATE, EDIT, ASIGN). <-- Param
    # body: Data general que va en cada cuerpo del correo y a quién va dirigido en variable body.to <-- Body
    # "ruben.kern@itprocesos.cl", "ecarrizo@fundacioncchc.cl" <-- Agregar a arreglo para pruebas de mañana.
    to = ["jonathan.diaz@itprocesos.cl", "eduardo.molina@itprocesos.cl"]
    # create message object instance
    msg = MIMEMultipart('alternative')
    # setup the parameters of the message
    password = "u8m7&KNJ4"
    msg['From'] = "fundacionsocialcchc@fundacioncchc.cl"
    msg['To'] = ','.join(to)
    html = ''
    #Obtaining type of message
    if(type == 'CREATE'):
        msg['Subject'] = f"Se creó caso social"
        html = f"""
                <html>
                    <head></head>
                    <body>
                        <p>Estimado(a)</p>\n
                        <p>El día INGRESAR_FECHA, <strong>INGRESAR_NOMBRE_QUIÉN_CREA_CASO_SOCIAL</strong>, profesional de la Fundación Social C.Ch.C., 
                        ha solicitado analizar autoderivación del caso de <strong>NOMBRE_QUIÉN_SE_ATENDIÓ</strong>, cédula de identidad N° RUT_QUIÉN_SE_ATENDIÓ, 
                        trabajador de la obra NOMBRE_OBRA de la empresa NOMBRE_EMPRESA.</p>\n
                        <p>El caso refiere lo siguiente:<p>\n
                        <p>COMENTARIO_EN_CREACIÓN_CASO_SOCIAL</p>\n
                        <p>De acuerdo a lo anterior se solicita:</p>\n
                        <p>COMENTARIO_CIERRE</p>\n
                        <div>Atentamente</div>
                        <div>Equipo Fundación Social C.Ch.C</div>
                    </body>
                </html>
                """
    if(type == 'EDIT'):
        msg['Subject'] = f"Se editó caso social"
        html = f"""
                <html>
                    <head></head>
                    <body>
                        <p>Estimado(a)</p>\n
                        <p>Equipo intervención caso N° NÚMERO_CASO</p>\n
                        <br/>
                        <p>El día INGRESAR_FECHA se ha modificado el programa de trabajo para el caso N° NÚMERO_CASO del trabajador:</p>\n
                        <p>R.U.T. N° INGRESAR_RUT, INGRESAR_NOMBRE.</p>\n
                        <p>Se agregaron las siguientes gestiones:</p>\n
                        <table style="width:100%; text-align:'center'">
                        <tr>
                            <th style="border-bottom:1px solid black"><strong>Gestión</strong></th>
                            <th style="border-bottom:1px solid black"><strong>Profesional</strong></th>
                            <th style="border-bottom:1px solid black"><strong>Fecha</strong></th>
                        </tr>
                        <tr>
                            <td style="border-bottom:1px solid black">TIPO_GESTIÓN</td>
                            <td style="border-bottom:1px solid black">NOMBRE_PROFESIONAL</td>
                            <td style="border-bottom:1px solid black">FECHA</td>
                        </tr>
                        </table>\n
                        <br/>
                        <div><strong>REFERENCIA:</strong></div>
                        <div>CASO N°: NÚMERO_CASO</div>
                        <div>FECHA: FECHA_CASO?</div>
                        <div>ÁREA: AREA_CASO</div>
                        <div>TEMA: TEMA_CASO</div>
                        <div>DERIVADO POR: QUIÉN_DERIVA_CASO</div>
                        <div>OFICINA: OFICINA_QUIÉN_DELEGA?</div>\n
                        <br/>
                        <div>Atentamente</div>
                        <div>Equipo Fundación Social C.Ch.C</div>
                    </body>
                </html>
                """
    if(type == 'ASIGN'):
        msg['Subject'] = f"Se asignó caso social"
        html = f"""
                <html>
                    <head></head>
                    <body>
                        <p>Estimado(a)</p>\n
                        <p>NOMBRE_DE_QUIÉN?</p>\n
                        <br/>
                        <p>El día INGRESAR_FECHA y tras revisar los antecedentes de la situación social derivada con el N° NÚMERO_CASO_SOCIAL, se ha 
                        resuelto abordar esta por el equipo de intervención de casos sociales.</p>\n
                        <p>En el análisis de la situación se observa que:</p>\n
                        <p><strong>COMENTARIO_DERIVACIÓN</strong></p>\n
                        <br/>
                        <p>Por tanto, para atender este caso, se ha seleccionado el siguiente equipo profesional:</p>\n
                        <ul>
                            <li>Susana Muñoz Loyola</li>
                            <li>Otra ejecutiva</li>
                            <li>Susana Muñoz Loyola</li>
                        </ul>\n
                        <br/>
                        <div>Atentamente</div>
                        <div>Equipo Fundación Social C.Ch.C</div>
                    </body>
                </html>
                """
    part2 = MIMEText(html, 'html')  
    msg.attach(part2)

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    
    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], to, msg.as_string())

    server.quit()
    
    print("successfully sent email to: ", msg['To'])