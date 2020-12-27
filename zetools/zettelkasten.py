from datetime import datetime


def generate() -> str:
    """Generates the zettelkasten ID for the current time."""
    return datetime.now().strftime("%Y%m%d%H%M%S")
