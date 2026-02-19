def is_valid_content(content: str) -> bool:
    if not content:
        return False

    if len(content) < 800:
        return False

    lowered = content.lower()

    # Detect bot protection pages
    blocked_signatures = [
        "enable javascript",
        "access denied",
        "request blocked",
        "captcha",
        "verify you are human"
    ]

    if any(sig in lowered for sig in blocked_signatures):
        return False

    if "<html" not in lowered:
        return False

    return True
