from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..analytics import analyze_notes

router = APIRouter()


@router.get("/")
def get_analytics(db: Session = Depends(get_db)):
    return analyze_notes(db)
