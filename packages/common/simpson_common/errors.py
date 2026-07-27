"""Standard exception hierarchy for Simpson Strong-Tie MCP."""


class SimpsonError(Exception):
    """Base exception for all Simpson Strong-Tie MCP errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class InsufficientInformationError(SimpsonError):
    """Raised when required engineering inputs or verified evidence are missing."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="INSUFFICIENT_INFORMATION")


class StorageError(SimpsonError):
    """Raised when an object storage operation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="STORAGE_ERROR")


class IngestionError(SimpsonError):
    """Raised when document parsing or claim extraction fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="INGESTION_ERROR")


class VerificationError(SimpsonError):
    """Raised when an engineering claim is unverified or rejected."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="VERIFICATION_ERROR")
