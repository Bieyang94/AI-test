from app.service.server.cache.base_cache import BaseCache
from app.service.server.config import get_settings

_outline_cache: BaseCache[str] = BaseCache(
    max_entries=get_settings().CACHE_MAX_ENTRIES,
    ttl_seconds=get_settings().CACHE_TTL_SECONDS,
)


def get_cached_outline(num: int) -> str | None:
    return _outline_cache.get(num)


def set_cached_outline(num: int, outline: str) -> None:
    _outline_cache.set(num, outline)


def delete_cached_outline(num: int) -> bool:
    return _outline_cache.delete(num)
