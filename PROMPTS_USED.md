# PROMPTS_USED.md

Below are representative prompts used during development.

---

## Architecture & Backend

- Design scalable FastAPI backend for competitive intelligence tracker
- Implement async SQLAlchemy session management with Neon
- Fix connection closed issue with asyncpg
- Add pool_pre_ping for serverless Postgres
- Implement diff percentage calculation between text snapshots
- Add significant change flag logic
- Implement LLM skip logic if change < 2%
- Add Playwright fallback for JS-heavy websites
- Build status endpoint to check backend, DB, and LLM health

---

## LLM & Summarization

- Improve prompt for summarizing website diffs
- Generate structured business-focused summary from diff text
- Optimize LLM cost by skipping small diffs
- Format LLM output for frontend display

---

## Deployment

- Configure Render deployment for FastAPI
- Fix SSL issues for Neon with asyncpg
- Add CORS middleware for frontend communication
- Install Playwright chromium in Render build step
- Create Dockerfile with Playwright support

---

## Frontend

- Build minimal React dashboard for FastAPI backend
- Improve UI styling for SaaS look
- Format LLM summary into structured bullets
- Add status health bar
- Add modal for check history display

---

## Documentation

- Create submission-ready README
- Define deliverables checklist
