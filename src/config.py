import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

# Load .env file if present
load_dotenv()


def get_settings() -> Dict[str, str]:
    """Return application settings from environment variables."""
    settings = {
        "jira_base_url": os.getenv("JIRA_BASE_URL", "").strip(),
        "jira_email": os.getenv("JIRA_EMAIL", "").strip(),
        "jira_api_token": os.getenv("JIRA_API_TOKEN", "").strip(),
        "jira_verify_ssl": os.getenv("JIRA_VERIFY_SSL", "true").lower() != "false",
        "jira_default_jql": os.getenv("JIRA_JQL"),
        "report_output_dir": os.getenv("REPORT_OUTPUT_DIR", "./outputs/reports"),
        "summary_output_dir": os.getenv("SUMMARY_OUTPUT_DIR", "./outputs/summaries"),
        "log_output_dir": os.getenv("LOG_OUTPUT_DIR", "./outputs/logs"),
    }

    _ensure_directories(settings)
    _warn_missing_jira(settings)
    return settings


def _ensure_directories(settings: Dict[str, str]) -> None:
    dirs = [
        settings["report_output_dir"],
        settings["summary_output_dir"],
        settings["log_output_dir"],
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def _warn_missing_jira(settings: Dict[str, str]) -> None:
    missing = []
    if not settings["jira_base_url"]:
        missing.append("JIRA_BASE_URL")
    if not settings["jira_email"]:
        missing.append("JIRA_EMAIL")
    if not settings["jira_api_token"]:
        missing.append("JIRA_API_TOKEN")
    if missing:
        print("[WARNING] Missing required Jira variables:", ", ".join(missing))
