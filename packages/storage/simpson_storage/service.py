"""Object storage interface and filesystem implementation."""

from abc import ABC, abstractmethod
from pathlib import Path

from simpson_common.errors import StorageError


class ObjectStorageService(ABC):
    """Abstract interface for immutable object storage."""

    @abstractmethod
    async def put_object(self, object_key: str, content: bytes) -> str:
        """Store object binary content at object_key. Return object_key."""
        pass

    @abstractmethod
    async def get_object(self, object_key: str) -> bytes:
        """Retrieve object binary content at object_key."""
        pass

    @abstractmethod
    async def exists(self, object_key: str) -> bool:
        """Check if object exists."""
        pass


class FilesystemStorageService(ObjectStorageService):
    """Local filesystem adapter for object storage."""

    def __init__(self, root_dir: str = "./data/storage") -> None:
        self.root_path = Path(root_dir).resolve()
        self.root_path.mkdir(parents=True, exist_ok=True)

    def _get_path(self, object_key: str) -> Path:
        target = (self.root_path / object_key).resolve()
        if not str(target).startswith(str(self.root_path)):
            raise StorageError(f"Path traversal detected for key: {object_key}")
        return target

    async def put_object(self, object_key: str, content: bytes) -> str:
        file_path = self._get_path(object_key)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)
        return object_key

    async def get_object(self, object_key: str) -> bytes:
        file_path = self._get_path(object_key)
        if not file_path.is_file():
            raise StorageError(f"Object not found: {object_key}")
        return file_path.read_bytes()

    async def exists(self, object_key: str) -> bool:
        file_path = self._get_path(object_key)
        return file_path.is_file()
