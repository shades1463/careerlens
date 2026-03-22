import re

def clean_text(text: str) -> str:
    """Remove HTML tags, URLs, special characters, and extra whitespace."""
    text = re.sub(r'<[^>]*?>', '', text)          # HTML tags
    text = re.sub(r'http[s]?://\S+', '', text)     # URLs
    text = re.sub(r'[^a-zA-Z0-9 .,()\-]', ' ', text)  # special chars
    text = re.sub(r'\s+', ' ', text).strip()       # extra whitespace
    return text