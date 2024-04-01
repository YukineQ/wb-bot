from config import config
from core.helpers.cache import Cache, FileBackend, RedisBackend
from chat_bot.bot import run_bot


def init_cache() -> None:
    cache_methods = {
        "file": FileBackend(config.JSON_FILE_NAME),
        "redis": RedisBackend()
    }

    Cache.init(backend=cache_methods[config.CACHE_METHOD])


if __name__ == '__main__':
    init_cache()
    run_bot()
