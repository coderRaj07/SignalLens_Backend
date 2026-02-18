from fastapi import APIRouter
from sqlalchemy import text
from app.db.database import engine
from app.services.llm.factory import get_llm_provider

router = APIRouter()

@router.get("/")
async def status():

    db_status = "healthy"
    llm_status = "healthy"

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"

    try:
        llm = get_llm_provider()
        await llm.chat("Respond with OK")
    except Exception:
        llm_status = "unhealthy"

    return {
        "backend": "healthy",
        "database": db_status,
        "llm": llm_status
    }
