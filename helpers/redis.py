import redis

redis_db = redis.Redis(host='localhost', port=6379, decode_responses=True)


def get_chat_keys(pattern: str = '*'):
    return redis_db.keys(pattern=pattern)


def get_chat_id_by_key(key: str):
    return redis_db.get(key)


def set_chat_id(key: str, *, val: str):
    redis_db.set(key, val)


def delete_chat_by_key(key: str):
    redis_db.delete(key)
