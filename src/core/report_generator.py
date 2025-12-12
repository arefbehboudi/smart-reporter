from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

from src.config import get_settings
from src.core.analyzer import analyze_issues, format_summary
from src.core.clients.jira_client import JiraClient
from src.models.issue import Issue


def fetch_from_jira(settings: dict) -> Iterable[Issue]:
    """Instantiate Jira client and fetch issues with optional default JQL."""
    client = JiraClient(
        base_url=settings["jira_base_url"],
        email=settings["jira_email"],
        api_token=settings["jira_api_token"],
        verify_ssl=settings["jira_verify_ssl"],
    )
    return client.fetch_issues(jql=settings["jira_default_jql"])


def run(jql: Optional[str] = None) -> Path:
    """Generate a text report from Jira issues and return the output path."""
    settings = get_settings()

    effective_settings = dict(settings)
    effective_settings["jira_default_jql"] = jql or settings.get("jira_default_jql")

    issues = fetch_from_jira(effective_settings)
    summary = analyze_issues(issues)
    summary_text = format_summary(summary)

    output_dir = Path(settings["summary_output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = output_dir / f"report-{timestamp}.txt"
    output_file.write_text(summary_text, encoding="utf-8")

    return output_file
