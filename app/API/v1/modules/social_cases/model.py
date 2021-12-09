from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String
from ..intervention_plans.model import InterventionPlan


class SocialCase(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "social_case"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date = Column(DateTime(timezone=True), nullable=False)
    assistance_id = Column(Integer, nullable=False)
    employee_rut = Column(String(12), nullable=False)
    employee_id = Column(Integer, nullable=False)
    employee_names = Column(String(250), nullable=False)
    business_id = Column(Integer, nullable=False)
    business_name = Column(String(200), nullable=False)
    office = Column(String(120), nullable=False)
    state = Column(String(25), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    area_id = Column(Integer, nullable=False)
    delegation = Column(String(120), nullable=False)
    professional_id = Column(Integer, nullable=False)
    zone = Column(String(120))

    intervention_plans = relationship(
        "InterventionPlan", back_populates="social_case", lazy="select")
