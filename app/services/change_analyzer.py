import difflib

def calculate_change_percentage(old: str, new: str) -> float:
    matcher = difflib.SequenceMatcher(None, old, new)
    similarity = matcher.ratio()
    change_percentage = (1 - similarity) * 100
    return round(change_percentage, 2)


def is_significant_change(change_percentage: float, threshold: float = 10.0) -> bool:
    """
    Default threshold = 10%
    Can adjust later.
    """
    return change_percentage >= threshold
