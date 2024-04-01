from typing import Any
import atexit

from core.helpers.cache.base import BaseBackend


class JsonReaderMixin:
    import json

    def read_from_json(self, file_name: str) -> Any:
        with open(file_name, 'r') as f:
            json_file = f.read()

        return self.json.loads(json_file)


class JsonWriterMixin:
    import json

    def write_to_json(self, data: Any, file_name: str) -> None:
        if not isinstance(data, dict):
            return

        with open(file_name, 'w') as f:
            f.truncate()
            self.json.dump(data, f)
            f.truncate()


class FileBackend(
    BaseBackend,
    JsonReaderMixin,
    JsonWriterMixin,
):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

        try:
            self.cache = self.read_from_json(self.file_name)
        except (IOError, ValueError):
            self.cache = {}

        atexit.register(lambda: self.write_to_json(self.cache, self.file_name))

    async def get(self, *, key: str) -> Any:
        result = self.cache.get(key)

        if not result:
            return

        return result

    async def get_keys(self) -> Any:
        return self.cache.keys()

    async def set(self, *, key: str, val: str) -> Any:
        if not self.cache.get(key):
            self.cache[key] = val

    async def delete(self, *, key: str) -> Any:
        del self.cache[key]
