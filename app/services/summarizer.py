import re
import json
from app.services.llm.factory import get_llm_provider

MAX_DIFF_CHARS = 8000

# ---------------- Pricing patterns (supports decimals) ----------------
PRICE_PATTERN = r"\$\d+(?:\.\d+)?|\₹\d+(?:\.\d+)?|\€\d+(?:\.\d+)?|\d+(?:\.\d+)?\s?(USD|INR|EUR)"

PRICE_KEYWORDS = [
    "price", "pricing", "plan", "subscription",
    "per month", "per year", "billing", "annual"
]

# ---------------- Docs / API patterns ----------------
API_KEYWORDS = [
    "api", "endpoint", "request", "response", "parameter",
    "authentication", "token", "sdk", "version", "v1", "v2"
]

# ---------------- Changelog / Release patterns ----------------
CHANGELOG_KEYWORDS = [
    "release", "released", "added", "removed",
    "deprecated", "breaking change", "bug fix",
    "improvement", "update", "changelog"
]


async def summarize_diff(diff: str, change_percentage: float, url: str):

    # ---------------- Empty Diff ----------------
    if not diff.strip():
        return {
            "significant": False,
            "change_types": [],
            "summary": "No meaningful changes detected.",
            "confidence": 100
        }

    diff_lower = diff.lower()

    # ---------------- Detect Pricing Signal ----------------
    numeric_price_detected = re.search(PRICE_PATTERN, diff)
    pricing_keyword_detected = any(k in diff_lower for k in PRICE_KEYWORDS)
    pricing_signal = bool(numeric_price_detected or pricing_keyword_detected)

    # ---------------- Detect Docs/API Signal ----------------
    docs_signal = any(k in diff_lower for k in API_KEYWORDS)

    # ---------------- Detect Changelog Signal ----------------
    changelog_signal = any(k in diff_lower for k in CHANGELOG_KEYWORDS)

    # ---------------- Force LLM If Important Semantic Signal ----------------
    force_llm = pricing_signal or docs_signal or changelog_signal

    # ---------------- Skip Tiny Noise Unless Important ----------------
    if change_percentage < 2.0 and not force_llm:
        return {
            "significant": False,
            "change_types": [],
            "summary": "Change too small — LLM skipped for cost optimization.",
            "confidence": 100
        }

    # ---------------- Prevent Token Explosion ----------------
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS]

    # ---------------- Dynamic Focus Instructions ----------------
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

    # ---------------- Build Prompt ----------------
    prompt = f"""
        You are analyzing a competitor website update.

        {focus_area}

        Return ONLY valid JSON in this format:

        {{
        "significant": true or false,
        "change_types": ["pricing", "features", "policy", "product", "docs", "changelog", "messaging", "other"],
        "summary": "Short executive summary in 3-5 bullet points",
        "confidence": 0-100
        }}

        Mark significant=true ONLY if there is:
        - Pricing change
        - Feature addition/removal
        - Product update
        - Policy update
        - Docs / API breaking change
        - Changelog item

        If changes are only UI/layout or trivial text edits → significant=false.

        Website Diff:
        {diff}
        """

    # ---------------- Call LLM ----------------
    try:
        llm = get_llm_provider()
        response = await llm.chat(prompt)

        try:
            parsed = json.loads(response)
            return parsed
        except Exception:
            return {
                "significant": False,
                "change_types": [],
                "summary": response.strip(),
                "confidence": 0
            }

    except Exception as e:
        return {
            "significant": False,
            "change_types": [],
            "summary": f"LLM summarization failed: {str(e)}",
            "confidence": 0
        }
