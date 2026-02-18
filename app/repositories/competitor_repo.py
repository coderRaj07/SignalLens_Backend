from sqlalchemy import select
from app.models.competitor import Competitor

class CompetitorRepository:

    async def create(self, db, data):
        competitor = Competitor(
            name=data.name,
            url=str(data.url), 
            tag=data.tag
        )

        db.add(competitor)
        await db.commit()
        await db.refresh(competitor)

        return competitor

    async def get(self, db, competitor_id):
        return await db.get(Competitor, competitor_id)

    async def list_all(self, db):
        result = await db.execute(select(Competitor))
        return result.scalars().all()
