from app.service.server.cache.base_cache import BaseCache
from app.service.server.config import get_settings

_xmind_cache: BaseCache[dict] = BaseCache(
    max_entries=get_settings().CACHE_MAX_ENTRIES,
    ttl_seconds=get_settings().CACHE_TTL_SECONDS,
)


def get_cached_xmind(num: int) -> dict | None:
    return _xmind_cache.get(num)


def set_cached_xmind(num: int, xmind_bytes: bytes, test_points: str) -> None:
    _xmind_cache.set(num, {"xmind_bytes": xmind_bytes, "test_points": test_points})


def delete_cached_xmind(num: int) -> bool:
    return _xmind_cache.delete(num)
