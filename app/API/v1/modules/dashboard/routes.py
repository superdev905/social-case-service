from sqlalchemy.sql.functions import func
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from app.database.main import get_database
from ...middlewares.auth import JWTBearer
from ..social_cases.model import SocialCase

router = APIRouter(prefix="/dashboard",
                   tags=["Dashboard"],
                   dependencies=[Depends(JWTBearer())])


@router.get("/stats")
def get_stats(db: Session = Depends(get_database)):

    result = []
    total = db.query(func.count(SocialCase.id).label("total")).filter(
        SocialCase.is_active == True).all()

    result.append({"label": "Total casos", "value": total[0].total})

    docs = db.query(func.count(SocialCase.id).label(
        "value"), SocialCase.state.label("label")).group_by(SocialCase.state).all()

    for i in docs:
        result.append({"label": i.label, "value": i.value})

    return result
