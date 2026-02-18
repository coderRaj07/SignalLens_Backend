from app.services.llm.factory import get_llm_provider

async def summarize_diff(diff: str, change_percentage: float) -> str:

    if change_percentage < 2.0:
        return "Change too small — LLM skipped for cost optimization."

    if not diff.strip():
        return "No meaningful changes detected."

    prompt = f"""
    Analyze this website diff.
    Highlight meaningful pricing, feature, or policy changes.
    Provide concise bullet points with quoted snippets.

    Diff:
    {diff}
    """

    try:
        llm = get_llm_provider()
        return await llm.chat(prompt)
    except Exception:
        return "LLM summarization failed."
