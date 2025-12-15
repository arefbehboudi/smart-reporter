from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from src.models.issue import Issue


class BaseClient(ABC):
    """Abstract data source client. Implement fetch_issues for your backend."""

    @abstractmethod
    def fetch_issues(self) -> Iterable[Issue]:
        """Return issues from the data source."""
        raise NotImplementedError

    def fetch_projects(self) -> List[str]:
        """Return available project keys or names."""
        raise NotImplementedError

    def fetch_statuses(self, project_key: Optional[str] = None) -> List[str]:
        """Return statuses (optionally scoped to a project)."""
        raise NotImplementedError

    def fetch_priorities(self) -> List[str]:
        """Return available priority names."""
        raise NotImplementedError

    def fetch_assignees(self, query: str = "") -> List[str]:
        """Return assignee display names, optionally filtered by a search query."""
        raise NotImplementedError

    def fetch_labels(self, query: str = "") -> List[str]:
        """Return label names, optionally filtered by a search prefix."""
        raise NotImplementedError
