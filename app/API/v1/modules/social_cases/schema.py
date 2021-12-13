from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from ...helpers.schema import AreaResponse, BussinessResponse, EmployeeResponse, User


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
    office: str = Field(alias="office")
    area_id: int = Field(alias="areaId")
    delegation: str
    zone: str

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
                "professionalId": 1
            }
        }


class SocialCaseItem(SocialCaseBase):
    id: int
    is_active: bool = Field(alias="isActive")
    created_at: datetime = Field(alias="createdDate")
    derivation_id: Optional[int] = Field(alias="derivationId")


class SocialCaseSimple(BaseModel):
    id: int
    date: datetime
    employee_names: str = Field(alias="employeeNames")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SocialCaseDetails(SocialCaseItem):
    business: BussinessResponse
    employee: EmployeeResponse
    area: AreaResponse
    professional: User
    closing: Optional[ClosingItem]
