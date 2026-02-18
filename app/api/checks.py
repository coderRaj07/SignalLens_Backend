from fastapi import APIRouter, BackgroundTasks
from app.services.check_service import CheckService
from app.repositories.check_repo import CheckRepository
from app.schemas.check import CheckOut
from app.db.session import AsyncSessionLocal

router = APIRouter()
service = CheckService()
repo = CheckRepository()

@router.post("/{competitor_id}")
async def check_now(competitor_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(service.run_check, competitor_id)
    return {"status": "processing"}

@router.get("/{competitor_id}", response_model=list[CheckOut])
async def get_last_5(competitor_id: int):
    async with AsyncSessionLocal() as db:
        return await repo.get_last_5(db, competitor_id)
