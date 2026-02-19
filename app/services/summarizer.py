from app.services.llm.factory import get_llm_provider

MAX_DIFF_CHARS = 8000  # protect token usage

async def summarize_diff(diff: str, change_percentage: float) -> str:

    # Cost optimization
    if change_percentage < 2.0:
        return "Change too small — LLM skipped for cost optimization."

    if not diff.strip():
        return "No meaningful changes detected."

    # Prevent token explosion
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS]

    prompt = f"""
        You are analyzing changes between two versions of a competitor's website.

        Analyze ALL meaningful changes including:

        - Pricing updates
        - Feature additions or removals
        - Product changes
        - Policy changes
        - Messaging updates
        - Positioning changes
        - Call-to-action (CTA) changes
        - Announcements
        - Structural content updates

        Ignore:
        - Pure HTML formatting differences
        - Minor whitespace changes
        - Tracking scripts
        - Metadata-only updates

        Respond in clear bullet points.

        If no meaningful business or structural change exists, reply exactly:
        "No meaningful business or structural changes detected."

        Change percentage: {change_percentage:.2f}%

        Website Diff:
        {diff}
        """

    try:
        llm = get_llm_provider()
        response = await llm.chat(prompt)
        return response.strip()

    except Exception as e:
        return f"LLM summarization failed: {str(e)}"
