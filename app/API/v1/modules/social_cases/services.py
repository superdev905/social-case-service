from typing import List
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import Session
from .schema import AssignedProfessional as ProfessionalSchema
from .model import AssignedProfessional
from app.settings import SERVICES
from ...helpers.fetch_data import fetch_service, handle_request


def create_professionals(db: Session, list: List[ProfessionalSchema], derivation_id: int, user_id: int):
    for i in list:
        new_item = jsonable_encoder(i, by_alias=False)
        new_item["derivation_id"] = derivation_id
        new_item["created_by"] = user_id

        db_item = AssignedProfessional(**new_item)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)


def get_assistance(req: Request, id: int):
    return fetch_service(req.token, SERVICES["assistance"]+"/assistance/"+str(id))


def patch_employee_status(req, employee_id: int, body):
    print(body)

    handle_request(req.token, SERVICES["employees"] +
                   "/employees/"+str(employee_id),
                   body,
                   "PATCH",)
