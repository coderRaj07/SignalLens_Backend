# AI_NOTES.md

## AI Tools Used

During development of SignalLens, I used the following AI tools:

- ChatGPT – architecture planning, debugging, refactoring suggestions
- LLM APIs (Cerebras) – generating competitive intelligence summaries

---

## Where AI Helped

AI assistance was used for:

- Designing scalable FastAPI project structure
- Implementing async SQLAlchemy patterns correctly
- Handling Neon database SSL issues
- Designing diff percentage calculation logic
- Implementing Playwright fallback strategy
- Improving frontend UI styling and UX polish
- Refining LLM summarization prompts

---

## What I Verified Manually

I manually verified and tested:

- Async DB session lifecycle correctness
- pool_pre_ping usage for Neon reliability
- Snapshot storage and retrieval logic
- Diff generation and percentage calculation
- Significant change threshold logic (>= 10%)
- Cost optimization rule (skip LLM if < 2% change)
- Playwright fallback for JS-heavy websites
- Proper CORS handling in production
- Production deployment on Render

---

## LLM Provider

**Provider Used:** Cerebras  
**Model:** llama3.1-8b  

### Why Cerebras?
- Low latency
- Simple API interface
- Cost-effective for summarization workloads
- OpenAI-compatible structure for flexibility

---

## Cost Optimization Strategy

To reduce unnecessary LLM calls:

- If change percentage < 2%
- LLM summarization is skipped
- A predefined message is stored instead

This avoids unnecessary token usage.

---

## Architectural Decisions

- FastAPI for async backend
- SQLAlchemy (Async) for DB operations
- Neon PostgreSQL (serverless)
- Playwright for dynamic content fallback
- React (Vite) frontend
- REST-based integration between frontend & backend

---

## Final Note

All core logic (diff calculation, snapshot versioning, change thresholds, and backend reliability) was reviewed and tested manually to ensure correctness beyond AI-generated suggestions.
