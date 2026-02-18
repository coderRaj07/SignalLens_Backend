from fastapi import FastAPI
from app.api import competitors, checks, status
from app.models import Base
from app.db.database import engine

app = FastAPI(title="Competitive Intelligence Tracker")

app.include_router(competitors.router, prefix="/competitors")
app.include_router(checks.router, prefix="/checks")
app.include_router(status.router, prefix="/status")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
