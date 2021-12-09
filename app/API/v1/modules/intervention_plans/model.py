from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String


class InterventionPlan(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "intervention_plan"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    next_date = Column(DateTime(timezone=True), nullable=False)
    frequency = Column(String(15), nullable=False)
    social_case_id = Column(Integer, ForeignKey(
        "social_case.id"), nullable=False)
    management_id = Column(Integer, nullable=False)
    management_name = Column(String(120), nullable=False)
    professional_id = Column(Integer, nullable=False)
    professional_names = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    social_case = relationship(
        "SocialCase", back_populates="intervention_plans", lazy="select")
