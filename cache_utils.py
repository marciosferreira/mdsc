"""Cache simples em memória com TTL.

Usado pelos endpoints de leitura do router `brazil` para evitar repetir,
a cada refresh do dashboard, várias queries sequenciais ao Postgres
(cada round-trip custa ~190ms neste ambiente, mesmo para queries triviais).
"""

import threading
import time
from functools import wraps

_lock = threading.Lock()
_store: dict = {}


def ttl_cache(ttl: float = 20.0):
    """Cacheia o retorno da função por `ttl` segundos, por combinação de argumentos."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = (fn.__module__, fn.__qualname__, args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            with _lock:
                cached = _store.get(key)
                if cached and now - cached[1] < ttl:
                    return cached[0]
            result = fn(*args, **kwargs)
            with _lock:
                _store[key] = (result, now)
            return result
        return wrapper
    return decorator


def clear_all():
    """Remove todas as entradas do cache (chamado após reset diário / shift de datas)."""
    with _lock:
        _store.clear()
