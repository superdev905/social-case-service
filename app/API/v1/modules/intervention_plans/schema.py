from datetime import datetime
from pydantic import BaseModel, Field
from ...helpers.schema import EmployeeResponse, User
from ..social_cases.schema import SocialCaseItem


class PlanBase(BaseModel):
    frequency: str
    next_date: datetime = Field(alias="nextDate")
    social_case_id: int = Field(alias="socialCaseId")
    management_id: int = Field(alias="managementId")
    management_name: str = Field(alias="managementName")
    professional_id: int = Field(alias="professionalId")
    professional_names: str = Field(alias="professionalNames")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PlanCreate(PlanBase):
    class Config:
        schema_extra = {
            "example": {
                "frequency": "FECHA FIJA",
                "nextDate": datetime.now(),
                "socialCaseId": 1,
                "managementId": 1,
                "managementName": "SALUD",
                "professionalId": 1,
                "professionalNames": "JHON DOE DOE",

            }
        }


class PlanItem(PlanBase):
    id: int
    is_active: bool = Field(alias="isActive")
    is_completed: bool = Field(alias="isCompleted")
    created_at: datetime = Field(alias="createdDate")


class SocialCaseEmployee(SocialCaseItem):
    employee: EmployeeResponse


class PlanDetails(PlanItem):
    social_case: SocialCaseEmployee = Field(alias="socialCase")
    professional: User
