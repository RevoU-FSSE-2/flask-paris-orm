from datetime import datetime, timezone


def now():
    """Get the current UTC date and time."""
    return datetime.now(timezone.utc)
