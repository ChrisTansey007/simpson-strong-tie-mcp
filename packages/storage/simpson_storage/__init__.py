"""Immutable object storage abstraction and SHA-256 hash calculator."""

from simpson_storage.hasher import calculate_sha256, generate_object_key
from simpson_storage.service import FilesystemStorageService, ObjectStorageService

__all__ = [
    "calculate_sha256",
    "generate_object_key",
    "ObjectStorageService",
    "FilesystemStorageService",
]
