from __future__ import annotations

from typing import List, Optional

import pandas as pd
import streamlit as st

from src.config import get_settings
from src.core.analyzer import analyze_issues
from src.core.clients.jira_client import JiraClient
from src.dashboard.charts.bar import render_bar_chart
from src.dashboard.components.filters import render_filters
from src.dashboard.components.tables import issues_to_rows, render_blockers_table, render_issues_table
from src.models.issue import Issue


def _bounded_default_jql(project_keys: Optional[List[str]]) -> str:
    if project_keys:
        keys = ",".join(project_keys)
        return f"project IN ({keys}) ORDER BY updated DESC"
    return "updated >= -30d ORDER BY updated DESC"


def main() -> None:
    st.set_page_config(page_title="Smart Reporter Dashboard", layout="wide")
    st.title("Smart Reporter Dashboard")

    settings = get_settings()
    if not settings["jira_base_url"] or not settings["jira_email"] or not settings["jira_api_token"]:
        st.error("Missing Jira configuration. Please set JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN.")
        return

    # -------------------------
    # Sidebar - Filters (component)
    # -------------------------
    filters, should_fetch = render_filters(settings)

    # -------------------------
    # Fetch & Cache in session_state
    # -------------------------
    if should_fetch:
        try:
            client = JiraClient(
                base_url=settings["jira_base_url"],
                email=settings["jira_email"],
                api_token=settings["jira_api_token"],
                verify_ssl=settings["jira_verify_ssl"],
            )

            final_jql = filters["custom_jql"]
            if not final_jql:
                if any([
                    filters["project_keys"],
                    filters["statuses"],
                    filters["priorities"],
                    filters["assignees"],
                    filters["labels"],
                    filters["text_search"],
                ]):
                    final_jql = None
                else:
                    final_jql = _bounded_default_jql(filters["project_keys"])

            issues = list(
                client.fetch_issues(
                    jql=final_jql,
                    project_keys=filters["project_keys"],
                    statuses=filters["statuses"],
                    priorities=filters["priorities"],
                    assignees=filters["assignees"],
                    labels=filters["labels"],
                    text_search=filters["text_search"],
                    max_results=filters["max_results"],
                )
            )

            st.session_state["issues"] = issues

        except Exception as exc:  # noqa: BLE001
            st.error(f"Failed to fetch issues: {exc}")
            return

    issues: List[Issue] = st.session_state.get("issues", [])

    if not issues:
        st.info("Set filters and click 'Fetch issues' to load data.")
        return

    # -------------------------
    # Analyze & Display
    # -------------------------
    summary = analyze_issues(issues)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total issues", summary["total"])
    col2.metric("Blockers", len(summary["blockers"]))
    col3.metric("Unique statuses", len(summary["statuses"]))

    # Charts
    st.subheader("By priority")
    pr_df = pd.DataFrame(
        [{"priority": k, "count": v} for k, v in (summary["priorities"] or {}).items()]
    )
    render_bar_chart(pr_df, "priority", "count", "Issues by priority")

    st.subheader("By status")
    st_df = pd.DataFrame(
        [{"status": k, "count": v} for k, v in (summary["statuses"] or {}).items()]
    )
    render_bar_chart(st_df, "status", "count", "Issues by status")

    # Blockers
    if summary["blockers"]:
        st.subheader("Current blockers")
        blockers_rows = issues_to_rows(summary["blockers"], settings["jira_base_url"])
        render_blockers_table(blockers_rows)

    st.subheader("All issues")
    rows = issues_to_rows(issues, settings["jira_base_url"])
    render_issues_table(rows)


if __name__ == "__main__":
    main()
