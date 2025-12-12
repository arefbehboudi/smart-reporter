from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from src.models.issue import Issue


class BaseClient(ABC):
    """Abstract data source client. Implement fetch_issues for your backend."""

    @abstractmethod
    def fetch_issues(self) -> Iterable[Issue]:
        """Return issues from the data source."""
        raise NotImplementedError
