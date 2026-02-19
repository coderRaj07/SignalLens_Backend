import difflib

def generate_diff(old: str, new: str, max_lines: int = 200) -> str:
    """
    Generate limited unified diff to avoid token explosion.
    """

    diff = list(
        difflib.unified_diff(
            old.splitlines(),
            new.splitlines(),
            lineterm=""
        )
    )

    # Limit diff size
    if len(diff) > max_lines:
        diff = diff[:max_lines]

    return "\n".join(diff)
