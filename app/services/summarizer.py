from app.services.llm.factory import get_llm_provider

MAX_DIFF_CHARS = 8000  # protect token usage

async def summarize_diff(diff: str, change_percentage: float) -> str:

    if change_percentage < 2.0:
        return "Change too small — LLM skipped for cost optimization."

    if not diff.strip():
        return "No meaningful changes detected."

    # Prevent token explosion
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS]

    prompt = f"""
                You are analyzing a competitor website update.

                Focus ONLY on:
                - Pricing changes
                - Feature additions or removals
                - Policy updates
                - Product updates

                Ignore:
                - Layout changes
                - HTML tags
                - Metadata
                - Small numeric changes (timestamps, vote counts, etc.)

                If no meaningful business change exists, reply exactly:
                "No significant business changes detected."

                Website Diff:
                {diff}
                """

    try:
        llm = get_llm_provider()
        response = await llm.chat(prompt)
        return response.strip()

    except Exception as e:
        return f"LLM summarization failed: {str(e)}"
