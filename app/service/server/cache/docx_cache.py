import io
import os

from app.service.server.cache.base_cache import BaseCache
from app.service.server.config import get_settings

ALLOWED_EXTENSIONS = {".md", ".docx", ".pdf"}

_file_cache: BaseCache[dict] = BaseCache(
    max_entries=get_settings().CACHE_MAX_ENTRIES,
    ttl_seconds=get_settings().CACHE_TTL_SECONDS,
)


def get_cached_file(num: int) -> dict | None:
    return _file_cache.get(num)


def set_cached_file(num: int, ext: str, raw_text: str) -> None:
    _file_cache.set(num, {"ext": ext, "raw_text": raw_text})


def delete_cached_file(num: int) -> bool:
    return _file_cache.delete(num)


def validate_file(filename: str) -> str:
    ext = os.path.splitext(filename)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"仅支持：{', '.join(sorted(ALLOWED_EXTENSIONS))}")
    return ext


async def read_file_to_text(file, ext: str) -> str:
    from app.core.tools.extract_word import extract_text_only as extract_docx_text
    from app.core.tools.extract_pdf import extract_text_only as extract_pdf_text

    raw_bytes = await file.read()
    max_size = get_settings().MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(raw_bytes) > max_size:
        raise ValueError(f"文件大小超过限制（最大{get_settings().MAX_UPLOAD_SIZE_MB}MB）")

    if ext == ".md":
        return raw_bytes.decode("utf-8", errors="ignore")
    elif ext == ".docx":
        return extract_docx_text(io.BytesIO(raw_bytes))
    elif ext == ".pdf":
        return extract_pdf_text(io.BytesIO(raw_bytes))
    else:
        raise ValueError(f"不支持的格式：{ext}")
