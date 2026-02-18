from sqlalchemy import select, desc
from app.models.check import Check

class CheckRepository:

    async def create(
        self,
        db,
        competitor_id,
        snapshot_id,
        diff,
        summary,
        change_percentage,
        is_significant
    ):
        check = Check(
            competitor_id=competitor_id,
            snapshot_id=snapshot_id,
            diff=diff,
            summary=summary,
            change_percentage=change_percentage,
            is_significant=is_significant
        )
        db.add(check)
        await db.commit()
        await db.refresh(check)
        return check

    async def get_last_5(self, db, competitor_id):
        result = await db.execute(
            select(Check)
            .where(Check.competitor_id == competitor_id)
            .order_by(desc(Check.created_at))
            .limit(5)
        )
        return result.scalars().all()
