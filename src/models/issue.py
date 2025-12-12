from pydantic import BaseModel


class Issue(BaseModel):
    """Simple issue model used for early data and analysis."""

    id: str
    title: str
    status: str
    priority: str = "Medium"
    assignee: str | None = None
    is_blocker: bool = False
