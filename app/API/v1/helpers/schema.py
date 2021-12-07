from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from pydantic.errors import EmailError
from sqlalchemy.orm import relationship


class SuccessResponse(BaseModel):
    message: str


class User (BaseModel):
    id: int
    names: str
    paternal_surname: str = Field(alias='paternalSurname')
    maternal_surname: str = Field(alias='maternalSurname')


class PaginationResponse (BaseModel):
    page: int
    size: int
    total: int


class EmployeeResponse(BaseModel):
    run: str
    id: int
    names: str
    paternal_surname: str = Field(alias="paternalSurname")
    maternal_surname: str = Field(alias="maternalSurname")
    gender: str

    class Config:
        allow_population_by_field_name = True


class BussinessResponse(BaseModel):
    rut: str
    id: int
    address: str
    email: str
    business_name: str = Field(alias="businessName")

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

    class Config:
        allow_population_by_field_name = True


class BussinessResponse(BaseModel):
    rut: str
    id: int
    address: str
    email: str
    type: str
    business_name: str = Field(alias="businessName")
    region: Region
    commune: Commune
    interlocutor: Optional[Interlocutor]

    class Config:
        allow_population_by_field_name = True
