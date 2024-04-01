import redis

from config import config

redis_client = redis.from_url(
    url=f"redis://{config.REDIS_HOST}", decode_responses=True)
