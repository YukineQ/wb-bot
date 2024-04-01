from abc import ABC, abstractmethod
from typing import Any


class BaseBackend(ABC):
    @abstractmethod
    async def get(self, *, key: str) -> Any:
        """Get"""

    @abstractmethod
    async def get_keys(self) -> Any:
        """Get keys"""

    @abstractmethod
    async def set(self, *, key: str) -> Any:
        """Set"""

    @abstractmethod
    async def delete(self, *, key: str) -> Any:
        """Delete"""
