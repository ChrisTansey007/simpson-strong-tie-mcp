"""SHA-256 calculator and immutable object key generator."""

import hashlib


def calculate_sha256(content: bytes) -> str:
    """Calculate hex SHA-256 hash of binary content."""
    return hashlib.sha256(content).hexdigest()


def generate_object_key(
    publisher: str, document_key: str, sha256_hash: str, filename: str = "original.pdf"
) -> str:
    """Generate structured immutable object key path: sources/{pub}/{doc_key}/{sha256}/{filename}."""
    clean_pub = publisher.lower().replace(" ", "_")
    clean_key = document_key.lower().replace(" ", "_")
    return f"sources/{clean_pub}/{clean_key}/{sha256_hash}/{filename}"
