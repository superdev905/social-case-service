from datetime import datetime
from lib2to3.pgen2.token import OP
from typing import List, Optional
from pydantic import BaseModel, Field
from ...helpers.schema import AreaResponse, BussinessResponse, EmployeeResponse, Interlocutor, User


class AssignedProfessional(BaseModel):
    user_id: int = Field(alias="userId")
    fullname: str = Field(alias="fullName")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class AssignedProfessionalItem(AssignedProfessional):
    id: int


class DerivationBase(BaseModel):
    date: datetime
    assistance_titular_id: int = Field(alias="assistanceTitularId")
    observations: str
    state: str
    priority: str
    assigned_professionals: List[AssignedProfessional] = Field(
        alias="professionals")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class DerivationCreate(DerivationBase):
    pass


class DerivationItem(DerivationBase):
    assigned_professionals: Optional[List[AssignedProfessionalItem]] = Field(
        alias="professionals")


class DerivationDetails(DerivationBase):
    assigned_professionals: Optional[List[User]] = Field(
        alias="professionals")


class ClosingBase(BaseModel):
    date: datetime
    state: str
    professional_id: int = Field(alias="professionalId")
    professional_names: str = Field(alias="professionalNames")
    observations: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ClosingCreate(ClosingBase):
    pass


class ClosingItem(ClosingBase):
    id: int


class SocialCaseBase(BaseModel):
    date: datetime
    assistance_id: int = Field(alias="assistanceId")
    professional_id: int = Field(alias="professionalId")
    employee_rut: str = Field(alias="employeeRut")
    employee_id: int = Field(alias="employeeId")
    employee_names: str = Field(alias="employeeNames")
    business_id: int = Field(alias="businessId")
    business_name: str = Field(alias="businessName")
    construction_id: int = Field(alias="constructionId")
    construction_name: str = Field(alias="constructionName")
    area_id: int = Field(alias="areaId")
    request_type: str = Field(alias="requestType")
    derivation_state: Optional[str] = Field(alias="derivationState")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SocialCaseCreate(SocialCaseBase):
    class Config:
        schema_extra = {
            "example": {
                "date": datetime.now(),
                "assistanceId": 49,
                "employeeRut": "24.150.582-0",
                "employeeId": 41,
                "employeeNames": "TEST DE ERROR ERROR ERRORCITO",
                "businessId": 11,
                "businessName": "EMP 34",
                "office": "ANTOFAGASTA",
                "areaId": 2,
                "delegation": "ANTOFAGASTA",
                "zone": "ANTOFAGASTA",
                "professionalId": 1,
                "derivationState": "AUTODERIVACIÓN"
            }
        }


class SocialCaseItem(SocialCaseBase):
    id: int
    is_active: bool = Field(alias="isActive")
    state: str
    created_at: datetime = Field(alias="createdDate")
    derivation_id: Optional[int] = Field(alias="derivationId")

class DerivationStateId(SocialCaseBase):
    assistance_derivation_id: int = Field(alias='assistanceDerivationId')


class SocialCaseEmployee(SocialCaseItem):
    employee: EmployeeResponse
    motive: Optional[str]


class PlanItem(BaseModel):
    id: int
    management_id: int = Field(alias="managementId")
    management_name: str = Field(alias="managementName")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SocialCaseSimple(BaseModel):
    id: int
    date: datetime
    employee_names: str = Field(alias="employeeNames")
    employee_id: int = Field(alias="employeeId")
    intervention_plans: List[PlanItem] = Field(alias="interventionPlans")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SocialCaseDetails(SocialCaseItem):
    business: BussinessResponse
    employee: EmployeeResponse
    area: AreaResponse
    professional: User
    closing: Optional[ClosingItem]
