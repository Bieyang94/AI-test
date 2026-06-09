from app.service.server.cache.base_cache import BaseCache
from app.service.server.config import get_settings

_csv_cache: BaseCache[str] = BaseCache(
    max_entries=get_settings().CACHE_MAX_ENTRIES,
    ttl_seconds=get_settings().CACHE_TTL_SECONDS,
)


def get_cached_csv(num: int) -> str | None:
    return _csv_cache.get(num)


def set_cached_csv(num: int, csv_content: str) -> None:
    _csv_cache.set(num, csv_content)


def delete_cached_csv(num: int) -> bool:
    return _csv_cache.delete(num)
