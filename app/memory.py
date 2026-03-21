import os
USE_REDIS = True
try:
    import redis
except Exception:
    redis = None
    USE_REDIS = False

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
_r = None
_in_memory_store = {}

if USE_REDIS and redis is not None:
    try:
        _r = redis.from_url(REDIS_URL, decode_responses=True)
        _r.ping()
    except Exception:
        _r = None

def _push_in_memory(user_key, turn_text):
    lst = _in_memory_store.setdefault(user_key, [])
    lst.insert(0, turn_text)
    _in_memory_store[user_key] = lst[:3]

def _get_in_memory(user_key):
    return _in_memory_store.get(user_key, [])

def push_user_turn(user_id: str, turn_text: str):
    key = f"mem:{user_id}"
    if _r:
        try:
            _r.lpush(key, turn_text)
            _r.ltrim(key, 0, 2)
            return
        except Exception:
            pass
    _push_in_memory(key, turn_text)

def get_user_memory(user_id: str):
    key = f"mem:{user_id}"
    if _r:
        try:
            items = _r.lrange(key, 0, -1)
            return items or []
        except Exception:
            pass
    return _get_in_memory(key)
