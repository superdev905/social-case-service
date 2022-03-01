from datetime import datetime
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
    area_id: int = Field(alias="areaId")
    request_type: str = Field(alias="requestType")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SocialCaseCreate(SocialCaseBase):
    area_id: int = Field(alias="areaId"),
    assistance_id: int = Field(alias="assistanceId"),
    business_name: str = Field(alias="businessName"),
    date: datetime.now() = Fiel(alias="date"),
    employee_id: str = Field(alias="employeeId"),
    employee_names: str = Field(alias="employeeNames")
    employee_rut: str = Field(alias="employeeRut")
    profesional_id: str = Field(alias="profesionalId")
    request_type: str = Field(alias="requestType")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SocialCaseItem(SocialCaseBase):
    id: int
    is_active: bool = Field(alias="isActive")
    state: str
    created_at: datetime = Field(alias="createdDate")
    derivation_id: Optional[int] = Field(alias="derivationId")


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
