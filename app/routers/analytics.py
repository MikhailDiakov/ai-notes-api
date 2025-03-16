from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..analytics import analyze_notes

router = APIRouter()


@router.get("/")
async def get_analytics(db: AsyncSession = Depends(get_db)):
    return await analyze_notes(db)
