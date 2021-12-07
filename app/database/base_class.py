from typing import Any
from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer


@as_declarative()
class Base:
    id: Any
    def as_dict(self):
        return dict((c.name,
                     getattr(self, c.name))
                    for c in self.__table__.columns)
                    
@declarative_mixin
class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True),
                        nullable=False, server_default=func.now())
    @declared_attr
    def update_at(cls):
        return Column(DateTime(timezone=True),
                       onupdate=func.now(), server_default=func.now())
              
@declarative_mixin
class AuthorMixin:
    @declared_attr
    def created_by(cls):
        return Column(Integer, nullable=False)
    