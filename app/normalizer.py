import re


def normalize_text(text: str) -> str:
    if not text:
        return ""
    # Collapse whitespace
    text = " ".join(text.split())
    # Remove control characters
    text = re.sub(r"[\x00-\x1F\x7F]+", " ", text)
    return text.strip()


def extract_summary(text: str, max_chars: int = 1000) -> str:
    return normalize_text(text)[:max_chars]
