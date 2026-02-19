from app.services.content_cleaner import extract_main_content
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import AsyncSessionLocal
from app.services.fetcher import fetch_url
from app.services.diff_engine import generate_diff
from app.services.summarizer import summarize_diff
from app.services.change_analyzer import calculate_change_percentage, is_significant_change
from app.utils.hashing import hash_content
from app.repositories.snapshot_repo import SnapshotRepository
from app.repositories.check_repo import CheckRepository
from app.repositories.competitor_repo import CompetitorRepository


class CheckService:

    def __init__(self):
        self.snapshot_repo = SnapshotRepository()
        self.check_repo = CheckRepository()
        self.competitor_repo = CompetitorRepository()

    async def run_check(self, competitor_id: int):

        async with AsyncSessionLocal() as db:
            try:
                competitor = await self.competitor_repo.get(db, competitor_id)
                if not competitor:
                    return

                # ---------------- FETCH ----------------
                try:
                    raw_html = await fetch_url(competitor.url)
                    content = extract_main_content(raw_html)
                except Exception as e:
                    await self.check_repo.create(
                        db=db,
                        competitor_id=competitor_id,
                        snapshot_id=None,
                        diff="",
                        summary=f"Fetch failed: {str(e)}",
                        change_percentage=0.0,
                        is_significant=False
                    )
                    return

                content_hash = hash_content(content)
                last_snapshot = await self.snapshot_repo.get_latest(db, competitor_id)

                diff = ""
                summary = ""
                change_percentage = 0.0
                significant = False

                # ---------------- COMPARE ----------------
                if last_snapshot:
                    diff = generate_diff(last_snapshot.content, content)

                    change_percentage = calculate_change_percentage(
                        last_snapshot.content,
                        content
                    )

                    summary_data = await summarize_diff(
                        diff,
                        change_percentage,
                        competitor.url
                    )

                    summary = summary_data.get("summary", "")
                    semantic_significant = summary_data.get("significant", False)

                    numeric_significant = is_significant_change(change_percentage)

                    # Final decision
                    significant = semantic_significant or numeric_significant

                else:
                    summary = "Initial snapshot — no comparison available."
                    significant = False

                # ---------------- SAVE SNAPSHOT ----------------
                snapshot = await self.snapshot_repo.create(
                    db,
                    competitor_id,
                    content_hash,
                    content
                )

                # ---------------- SAVE CHECK ----------------
                await self.check_repo.create(
                    db,
                    competitor_id,
                    snapshot.id,
                    diff,
                    summary,
                    change_percentage,
                    significant
                )

            except SQLAlchemyError:
                await db.rollback()
                raise

            except Exception:
                await db.rollback()
                raise
