from __future__ import annotations

from typing import Iterable, List

import pandas as pd
import streamlit as st

from src.models.issue import Issue


def issues_to_rows(issues: Iterable[Issue], jira_base_url: str) -> List[dict]:
    base = jira_base_url.rstrip("/")
    rows = []
    for issue in issues:
        key = issue.id
        rows.append(
            {
                "id": key,
                "link": f"{base}/browse/{key}" if key else "",
                "title": issue.title,
                "status": issue.status,
                "priority": issue.priority,
                "assignee": issue.assignee or "-",
                "is_blocker": bool(issue.is_blocker),
            }
        )
    return rows


def render_blockers_table(rows: List[dict]) -> None:
    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "link": st.column_config.LinkColumn("Link", display_text="Open"),
            "is_blocker": st.column_config.CheckboxColumn("Is blocker"),
        },
    )


def render_issues_table(rows: List[dict]) -> None:
    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "link": st.column_config.LinkColumn("Link", display_text="Open"),
            "is_blocker": st.column_config.CheckboxColumn("Is blocker"),
        },
    )
