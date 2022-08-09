from datetime import datetime
from lib2to3.pgen2.token import OP
from typing import Optional
from pydantic import BaseModel, Field
from pydantic.errors import EmailError
from sqlalchemy.orm import relationship


class SuccessResponse(BaseModel):
    message: str


class User (BaseModel):
    id: int
    names: str
    email: str
    paternal_surname: str = Field(alias='paternalSurname')
    maternal_surname: str = Field(alias='maternalSurname')
    charge_name: Optional[str] = Field(alias='charge')


class PaginationResponse (BaseModel):
    page: int
    size: int
    total: int


class Nationality(BaseModel):
    description: str
    id: int


class CurrentJob(BaseModel):
    admission_date: Optional[datetime] = Field(alias="admissionDate")
    business_id: Optional[int] = Field(alias="businessId")
    business_name: Optional[str] = Field(alias="businessName")
    construction_id: Optional[int] = Field(alias="constructionId")
    construction_name: Optional[str] = Field(alias="constructionName")
    salary: Optional[float]


class EmployeeResponse(BaseModel):
    id: int
    names: str
    paternal_surname: str = Field(alias="paternalSurname")
    maternal_surname: str = Field(alias="maternalSurname")
    gender: str
    nationality: Nationality
    current_job: Optional[CurrentJob] = Field(alias="currentJob")

    class Config:
        allow_population_by_field_name = True


class BeneficiaryResponse(BaseModel):
    run: Optional[str]
    id: int
    names: str
    relationship: Optional[str]
    is_relative: bool = Field(alias="isRelative")
    paternal_surname: str = Field(alias="paternalSurname")
    maternal_surname: str = Field(alias="maternalSurname")

    class Config:
        allow_population_by_field_name = True


class Region(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Commune(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Interlocutor(BaseModel):
    id: int
    full_name: str
    charge_id: int
    charge_name: str
    email: str
    cell_phone: str
    office_phone: str
    other_phone: str
    business_id: int
    is_interlocutor: bool
    created_at: datetime

    class Config:
        allow_population_by_field_name = True


class BussinessResponse(BaseModel):
    rut: str
    id: int
    address: str
    email: Optional[str]
    type: str
    business_name: str = Field(alias="businessName")
    region: Region
    commune: Commune
    interlocutor: Optional[Interlocutor]

    class Config:
        allow_population_by_field_name = True


class AreaResponse(BaseModel):
    id: int
    name: str

    class Config:
        allow_population_by_field_name = True

class TemaResponse(BaseModel):
    id: int
    name: str