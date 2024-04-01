from core.helpers.cache.base import BaseBackend


class CacheManager:
    def __init__(self):
        self.backend = None

    def init(self, *, backend: BaseBackend) -> None:
        self.backend = backend


Cache = CacheManager()
