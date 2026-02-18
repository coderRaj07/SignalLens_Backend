from fastapi import APIRouter, Depends
from app.schemas.competitor import CompetitorCreate, CompetitorOut
from app.db.session import get_db
from app.repositories.competitor_repo import CompetitorRepository

router = APIRouter()
repo = CompetitorRepository()

@router.post("/", response_model=CompetitorOut)
async def create_competitor(data: CompetitorCreate, db=Depends(get_db)):
    return await repo.create(db, data)

@router.get("/", response_model=list[CompetitorOut])
async def list_competitors(db=Depends(get_db)):
    return await repo.list_all(db)
