def is_valid_content(content: str) -> bool:
    if not content or len(content) < 1000:
        return False

    lowered = content.lower()

    if "enable javascript" in lowered:
        return False

    if '<div id="root"></div>' in lowered:
        return False

    return True
