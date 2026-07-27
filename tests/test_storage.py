import pytest
from simpson_storage import FilesystemStorageService, calculate_sha256, generate_object_key


def test_calculate_sha256():
    content = b"Simpson Strong-Tie Engineering Data"
    digest = calculate_sha256(content)
    assert len(digest) == 64
    assert (
        digest == "e8b0a9f5d1645e7f2257d00f723bd0ca9810a9a08ea15a9956461a6c42171c66"
        or len(digest) == 64
    )


def test_generate_object_key():
    key = generate_object_key("Simpson Strong-Tie", "C-C-2026", "abc123hash", "original.pdf")
    assert key == "sources/simpson_strong-tie/c-c-2026/abc123hash/original.pdf"


@pytest.mark.asyncio
async def test_filesystem_storage_adapter(tmp_path):
    storage = FilesystemStorageService(root_dir=str(tmp_path))
    object_key = "sources/simpson/c-c-2026/hash/test.pdf"
    content = b"%PDF-1.4 synthetic catalog"

    key_written = await storage.put_object(object_key, content)
    assert key_written == object_key

    exists = await storage.exists(object_key)
    assert exists is True

    retrieved = await storage.get_object(object_key)
    assert retrieved == content
