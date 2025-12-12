from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable, List

from src.models.issue import Issue


def analyze_issues(issues: Iterable[Issue]) -> Dict[str, object]:
    """Compute basic aggregates for a batch of issues."""
    issue_list: List[Issue] = list(issues)
    priorities = Counter(issue.priority for issue in issue_list)
    statuses = Counter(issue.status for issue in issue_list)
    blockers = [
        issue
        for issue in issue_list
        if issue.is_blocker or issue.status.lower() == "blocked"
    ]

    return {
        "total": len(issue_list),
        "priorities": priorities,
        "statuses": statuses,
        "blockers": blockers,
    }


def format_summary(summary: Dict[str, object]) -> str:
    """Render a human-readable text summary."""
    lines = [
        "Smart Reporter - Issue Summary",
        "-" * 32,
        f"Total issues: {summary['total']}",
        f"Blockers: {len(summary['blockers'])}",
        "",
        "By priority:",
    ]

    for priority, count in summary["priorities"].most_common():
        lines.append(f"  - {priority}: {count}")

    lines.append("")
    lines.append("By status:")
    for status, count in summary["statuses"].most_common():
        lines.append(f"  - {status}: {count}")

    if summary["blockers"]:
        lines.append("")
        lines.append("Current blockers:")
        for blocker in summary["blockers"]:
            lines.append(
                f"  - {blocker.id}: {blocker.title} (assignee: {blocker.assignee or 'unassigned'})"
            )

    return "\n".join(lines)
