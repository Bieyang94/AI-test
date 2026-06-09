from app.service.server.cache.docx_cache import get_cached_file, delete_cached_file
from app.service.server.cache.outLine_cache import get_cached_outline, delete_cached_outline
from app.service.server.cache.xmind_cache import get_cached_xmind, delete_cached_xmind
from app.service.server.cache.csv_cache import get_cached_csv, delete_cached_csv

_CACHE_MODULES = [
    ("文件", get_cached_file, delete_cached_file),
    ("大纲", get_cached_outline, delete_cached_outline),
    ("XMind", get_cached_xmind, delete_cached_xmind),
    ("CSV", get_cached_csv, delete_cached_csv),
]


def clear_all_caches(num: int) -> list[str]:
    deleted = []
    for name, getter, deleter in _CACHE_MODULES:
        if getter(num):
            deleter(num)
            deleted.append(name)
    return deleted
