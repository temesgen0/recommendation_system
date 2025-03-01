def preprocess_text(text: str) -> str:
    """
    Preprocess text for embedding generation.
    """
    # Convert to lowercase
    text = text.lower()
    # Remove special characters (optional)
    text = "".join(c for c in text if c.isalnum() or c.isspace())
    return text