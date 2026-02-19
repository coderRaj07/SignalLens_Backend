import re
from app.services.llm.factory import get_llm_provider

MAX_DIFF_CHARS = 8000

# Pricing patterns
PRICE_PATTERN = r"\$\d+|\₹\d+|\€\d+|\d+\s?(USD|INR|EUR)"
PRICE_KEYWORDS = ["price", "pricing", "plan", "subscription", "per month", "per year"]

# Docs / API patterns
API_KEYWORDS = [
    "api", "endpoint", "request", "response", "parameter",
    "authentication", "token", "sdk", "version", "v1", "v2"
]

# Changelog / Release patterns
CHANGELOG_KEYWORDS = [
    "release", "released", "added", "removed", "deprecated",
    "breaking change", "bug fix", "improvement", "update"
]

async def summarize_diff(diff: str, change_percentage: float, url: str) -> str:

    if not diff.strip():
        return "No meaningful changes detected."

    diff_lower = diff.lower()

    # -------- Detect Pricing Signal --------
    numeric_change_detected = re.search(PRICE_PATTERN, diff)
    pricing_keyword_detected = any(k in diff_lower for k in PRICE_KEYWORDS)
    pricing_signal = numeric_change_detected or pricing_keyword_detected

    # -------- Detect Docs/API Signal --------
    docs_signal = any(k in diff_lower for k in API_KEYWORDS)

    # -------- Detect Changelog Signal --------
    changelog_signal = any(k in diff_lower for k in CHANGELOG_KEYWORDS)

    # -------- Force Analysis If Important Semantic Signal --------
    force_llm = pricing_signal or docs_signal or changelog_signal

    # Skip tiny noise unless semantic trigger
    if change_percentage < 2.0 and not force_llm:
        return "Change too small — LLM skipped for cost optimization."

    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS]

    # -------- Build Focus Instructions --------
    focus_area = """
        Focus on meaningful business, product, pricing, documentation,
        API, or release-related changes.

        Ignore:
        - Cosmetic layout updates
        - Spacing changes
        - Minor HTML structure shifts
        """

    if pricing_signal:
        focus_area += """
        Pay special attention to pricing changes, subscription tiers,
        currency updates, billing intervals, and plan restructuring.
        """

    if docs_signal:
        focus_area += """
        Pay attention to API version changes, new endpoints,
        authentication changes, parameter updates, and SDK modifications.
        """

    if changelog_signal:
        focus_area += """
        Pay attention to newly added features, removed features,
        deprecated items, bug fixes, breaking changes,
        and release announcements.
        """

    prompt = f"""
        You are analyzing a competitor website update.

        {focus_area}

        Respond in concise bullet points.

        If no meaningful business change exists, respond:
        "No meaningful business changes detected."

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
