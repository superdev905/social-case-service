from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


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
