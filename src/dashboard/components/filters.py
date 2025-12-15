from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import streamlit as st

from src.core.clients.jira_client import JiraClient


@st.cache_data(ttl=300)
def _fetch_projects(base_url: str, email: str, api_token: str, verify_ssl: bool) -> List[str]:
    client = JiraClient(base_url=base_url, email=email, api_token=api_token, verify_ssl=verify_ssl)
    return client.fetch_projects()


@st.cache_data(ttl=300)
def _fetch_statuses(base_url: str, email: str, api_token: str, verify_ssl: bool, project_key: Optional[str]) -> List[str]:
    client = JiraClient(base_url=base_url, email=email, api_token=api_token, verify_ssl=verify_ssl)
    return client.fetch_statuses(project_key)


@st.cache_data(ttl=300)
def _fetch_priorities(base_url: str, email: str, api_token: str, verify_ssl: bool) -> List[str]:
    client = JiraClient(base_url=base_url, email=email, api_token=api_token, verify_ssl=verify_ssl)
    return client.fetch_priorities()


@st.cache_data(ttl=300)
def _fetch_assignees(base_url: str, email: str, api_token: str, verify_ssl: bool, query: str) -> List[str]:
    client = JiraClient(base_url=base_url, email=email, api_token=api_token, verify_ssl=verify_ssl)
    return client.fetch_assignees(query)


@st.cache_data(ttl=300)
def _fetch_labels(base_url: str, email: str, api_token: str, verify_ssl: bool, query: str) -> List[str]:
    client = JiraClient(base_url=base_url, email=email, api_token=api_token, verify_ssl=verify_ssl)
    return client.fetch_labels(query)


def _get_projects(settings: dict) -> List[str]:
    if "_projects_options" not in st.session_state:
        try:
            st.session_state["_projects_options"] = _fetch_projects(
                settings["jira_base_url"],
                settings["jira_email"],
                settings["jira_api_token"],
                settings["jira_verify_ssl"],
            )
        except Exception:
            st.sidebar.warning("Could not load projects; type manually.")
            st.session_state["_projects_options"] = []
    return st.session_state["_projects_options"]


def _get_statuses(settings: dict, project_key: Optional[str]) -> List[str]:
    statuses_cache = st.session_state.setdefault("_statuses_by_project", {})
    cache_key = project_key or "__global__"
    if cache_key not in statuses_cache:
        try:
            statuses_cache[cache_key] = _fetch_statuses(
                settings["jira_base_url"],
                settings["jira_email"],
                settings["jira_api_token"],
                settings["jira_verify_ssl"],
                project_key,
            )
        except Exception:
            st.sidebar.warning("Could not load statuses; type manually.")
            statuses_cache[cache_key] = []
    return statuses_cache.get(cache_key, [])


def _get_priorities(settings: dict) -> List[str]:
    if "_priorities_options" not in st.session_state:
        try:
            st.session_state["_priorities_options"] = _fetch_priorities(
                settings["jira_base_url"],
                settings["jira_email"],
                settings["jira_api_token"],
                settings["jira_verify_ssl"],
            )
        except Exception:
            st.sidebar.warning("Could not load priorities; type manually.")
            st.session_state["_priorities_options"] = []
    return st.session_state["_priorities_options"]


def _get_assignees(settings: dict) -> List[str]:
    if "_assignees_options" not in st.session_state:
        try:
            st.session_state["_assignees_options"] = _fetch_assignees(
                settings["jira_base_url"],
                settings["jira_email"],
                settings["jira_api_token"],
                settings["jira_verify_ssl"],
                "",
            )
        except Exception:
            st.sidebar.warning("Could not load assignees; type manually.")
            st.session_state["_assignees_options"] = []
    return st.session_state["_assignees_options"]


def _get_labels(settings: dict, query: str) -> List[str]:
    labels_cache = st.session_state.setdefault("_labels_by_query", {})
    cache_key = query or "__all__"
    if cache_key not in labels_cache:
        try:
            labels_cache[cache_key] = _fetch_labels(
                settings["jira_base_url"],
                settings["jira_email"],
                settings["jira_api_token"],
                settings["jira_verify_ssl"],
                query,
            )
        except Exception:
            st.sidebar.warning("Could not load labels; type manually.")
            labels_cache[cache_key] = []
    return labels_cache.get(cache_key, [])


def render_filters(settings: dict) -> Tuple[Dict[str, Optional[List[str]]], bool]:
    st.sidebar.header("Filters")

    auto_fetch = st.sidebar.checkbox("Auto-fetch on change", value=False, key="auto_fetch")

    custom_jql = st.sidebar.text_area(
        "Custom JQL (overrides filters)",
        value=settings.get("jira_default_jql", ""),
        height=80,
        key="custom_jql",
    )

    projects_options = _get_projects(settings)
    project_defaults = st.session_state.get("_project_defaults", [])
    project_keys = st.sidebar.multiselect(
        "Projects",
        options=projects_options,
        default=project_defaults,
        help="Select Jira projects (auto-loaded).",
        key="filter_projects",
    )
    if project_keys:
        st.session_state["_project_defaults"] = project_keys

    status_scope = project_keys[0] if project_keys else None
    statuses_options = _get_statuses(settings, status_scope) if project_keys else []
    statuses = st.sidebar.multiselect(
        "Statuses",
        options=statuses_options,
        default=[],
        help="Statuses from Jira; project-scoped when one project is selected.",
        key="filter_statuses",
    )

    priorities_options = _get_priorities(settings) if project_keys else []
    priorities = st.sidebar.multiselect(
        "Priorities",
        options=priorities_options,
        default=[],
        help="Priorities from Jira.",
        key="filter_priorities",
    )

    assignees_options = _get_assignees(settings) if project_keys else []
    assignees = st.sidebar.multiselect(
        "Assignees",
        options=assignees_options,
        default=[],
        help="Jira users.",
        key="filter_assignees",
    )

    label_query = st.sidebar.text_input("Label search", value="", key="label_query")
    labels_options = _get_labels(settings, label_query) if project_keys else []
    labels = st.sidebar.multiselect(
        "Labels",
        options=labels_options,
        default=[],
        help="Jira labels (search by prefix).",
        key="filter_labels",
    )

    text_search = st.sidebar.text_input("Text search", value="", key="text_search") or None
    max_results = st.sidebar.slider("Max results", min_value=10, max_value=200, value=50, step=10, key="max_results")

    st.sidebar.caption("Tip: If Custom JQL is set, other filters are ignored.")

    fetch_clicked = st.sidebar.button("Fetch issues", key="fetch_btn")

    filters = {
        "custom_jql": (custom_jql or "").strip(),
        "project_keys": project_keys or None,
        "statuses": statuses or None,
        "priorities": priorities or None,
        "assignees": assignees or None,
        "labels": labels or None,
        "text_search": text_search,
        "max_results": max_results,
    }

    current_filters_sig = (
        filters["custom_jql"],
        tuple(filters["project_keys"] or []),
        tuple(filters["statuses"] or []),
        tuple(filters["priorities"] or []),
        tuple(filters["assignees"] or []),
        tuple(filters["labels"] or []),
        filters["text_search"] or "",
        filters["max_results"],
    )
    prev_sig = st.session_state.get("_filters_sig")
    st.session_state["_filters_changed"] = prev_sig is not None and prev_sig != current_filters_sig
    st.session_state["_filters_sig"] = current_filters_sig

    should_fetch = fetch_clicked or (auto_fetch and st.session_state.get("_filters_changed", False))

    return filters, should_fetch
