from sqlalchemy import select, desc
from app.models.snapshot import Snapshot

class SnapshotRepository:

    async def create(self, db, competitor_id, content_hash, content):
        snapshot = Snapshot(
            competitor_id=competitor_id,
            content_hash=content_hash,
            content=content
        )
        db.add(snapshot)
        await db.commit()
        await db.refresh(snapshot)
        return snapshot

    async def get_latest(self, db, competitor_id):
        result = await db.execute(
            select(Snapshot)
            .where(Snapshot.competitor_id == competitor_id)
            .order_by(desc(Snapshot.created_at))
            .limit(1)
        )
        return result.scalar_one_or_none()
