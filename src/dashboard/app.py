from __future__ import annotations

from typing import Iterable, List, Optional

import pandas as pd
import streamlit as st
import altair as alt

from src.config import get_settings
from src.core.analyzer import analyze_issues
from src.core.clients.jira_client import JiraClient
from src.models.issue import Issue


def _parse_csv(value: str | None) -> Optional[List[str]]:
    if not value:
        return None
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or None


def _to_rows(issues: Iterable[Issue], jira_base_url: str) -> List[dict]:
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


def _bounded_default_jql(project_keys: Optional[List[str]]) -> str:
    # Jira Cloud ممکنه Unbounded JQL رو رد کنه، پس یه پیش‌فرض bounded داریم
    if project_keys:
        keys = ",".join(project_keys)
        return f"project IN ({keys}) ORDER BY updated DESC"
    return "updated >= -30d ORDER BY updated DESC"


def _bar_chart(df: pd.DataFrame, category_col: str, value_col: str, title: str) -> None:
    if df.empty:
        st.write("No data.")
        return

    # مرتب‌سازی برای خوانایی بهتر
    df = df.sort_values(value_col, ascending=False)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(f"{category_col}:N", sort="-y", title=None),
            y=alt.Y(f"{value_col}:Q", title=None),
            tooltip=[category_col, value_col],
        )
        .properties(height=260, title=title)
    )

    st.altair_chart(chart, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Smart Reporter Dashboard", layout="wide")
    st.title("Smart Reporter Dashboard")

    settings = get_settings()
    if not settings["jira_base_url"] or not settings["jira_email"] or not settings["jira_api_token"]:
        st.error("Missing Jira configuration. Please set JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN.")
        return

    # -------------------------
    # Sidebar - Filters
    # -------------------------
    st.sidebar.header("Filters")

    # UX: Auto fetch
    auto_fetch = st.sidebar.checkbox("Auto-fetch on change", value=False)

    custom_jql = st.sidebar.text_area(
        "Custom JQL (overrides filters)",
        value=settings.get("jira_default_jql", ""),
        height=80,
        placeholder='Example: project = "SB" AND status != Done ORDER BY updated DESC',
    )

    project_keys = _parse_csv(st.sidebar.text_input("Projects (comma separated keys)", value="SB"))

    # UX: برای فیلترهایی که احتمالاً لیست ثابت دارن، multiselect بهتره
    # ولی چون ما لیست real-time از Jira نمی‌گیریم، همچنان امکان CSV رو نگه می‌داریم.
    statuses = _parse_csv(st.sidebar.text_input("Statuses (comma separated)", value=""))
    priorities = _parse_csv(st.sidebar.text_input("Priorities (comma separated)", value=""))
    assignees = _parse_csv(st.sidebar.text_input("Assignees (comma separated)", value=""))
    labels = _parse_csv(st.sidebar.text_input("Labels (comma separated)", value=""))

    text_search = st.sidebar.text_input("Text search", value="") or None
    max_results = st.sidebar.slider("Max results", min_value=10, max_value=200, value=50, step=10)

    st.sidebar.caption("Tip: If Custom JQL is set, other filters are ignored.")

    fetch_clicked = st.sidebar.button("Fetch issues")

    # Auto-fetch trigger
    should_fetch = fetch_clicked or (auto_fetch and st.session_state.get("_filters_changed", False))

    # Track filter changes for auto-fetch
    # (هر رندر، بعد از first run، اگر auto_fetch روشن باشد و چیزی تغییر کند fetch می‌کنیم)
    current_filters_sig = (
        custom_jql,
        tuple(project_keys or []),
        tuple(statuses or []),
        tuple(priorities or []),
        tuple(assignees or []),
        tuple(labels or []),
        text_search or "",
        max_results,
    )
    prev_sig = st.session_state.get("_filters_sig")
    st.session_state["_filters_changed"] = prev_sig is not None and prev_sig != current_filters_sig
    st.session_state["_filters_sig"] = current_filters_sig

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

            # اگر Custom JQL خالیه، با فیلترها بساز
            # اما اگر هیچ فیلتری هم نیست، یک bounded پیش‌فرض می‌دیم تا Jira رد نکنه
            final_jql = (custom_jql or "").strip()
            if not final_jql:
                if any([project_keys, statuses, priorities, assignees, labels, text_search]):
                    final_jql = None  # یعنی از _build_jql خود client استفاده کن
                else:
                    final_jql = _bounded_default_jql(project_keys)

            issues = list(
                client.fetch_issues(
                    jql=final_jql,
                    project_keys=project_keys,
                    statuses=statuses,
                    priorities=priorities,
                    assignees=assignees,
                    labels=labels,
                    text_search=text_search,
                    max_results=max_results,
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

    # Charts (readable)
    st.subheader("By priority")
    pr_df = pd.DataFrame(
        [{"priority": k, "count": v} for k, v in (summary["priorities"] or {}).items()]
    )
    _bar_chart(pr_df, "priority", "count", "Issues by priority")

    st.subheader("By status")
    st_df = pd.DataFrame(
        [{"status": k, "count": v} for k, v in (summary["statuses"] or {}).items()]
    )
    _bar_chart(st_df, "status", "count", "Issues by status")

    # Blockers
    if summary["blockers"]:
        st.subheader("Current blockers")
        blockers_rows = _to_rows(summary["blockers"], settings["jira_base_url"])
        blockers_df = pd.DataFrame(blockers_rows)
        st.dataframe(
            blockers_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "link": st.column_config.LinkColumn("Link", display_text="Open"),
                "is_blocker": st.column_config.CheckboxColumn("Is blocker"),
            },
        )

    st.subheader("All issues")
    rows = _to_rows(issues, settings["jira_base_url"])
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


if __name__ == "__main__":
    main()
