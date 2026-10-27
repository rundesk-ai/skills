def display_name(first: str, last: str) -> str:
    """'Ada Quill' from its parts, ignoring surrounding spaces and an empty first name."""
    parts = [p.strip() for p in (first, last) if p and p.strip()]
    return " ".join(parts)
