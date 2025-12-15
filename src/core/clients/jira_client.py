from __future__ import annotations

from typing import Iterable, List, Optional

import requests
from requests.auth import HTTPBasicAuth

from src.core.clients.base_client import BaseClient
from src.models.issue import Issue


class JiraClient(BaseClient):
    """Jira REST client (v3) that maps issues to the local Issue model."""

    def __init__(
            self,
            base_url: str,
            email: str,
            api_token: str,
            verify_ssl: bool = True,
            timeout: int = 10,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.auth = HTTPBasicAuth(email, api_token)
        self.verify_ssl = verify_ssl
        self.timeout = timeout

    def fetch_issues(
            self,
            jql: Optional[str] = None,
            fields: Optional[List[str]] = None,
            max_results: int = 50,
            project_keys: Optional[List[str]] = None,
            statuses: Optional[List[str]] = None,
            priorities: Optional[List[str]] = None,
            assignees: Optional[List[str]] = None,
            labels: Optional[List[str]] = None,
            text_search: Optional[str] = None,
    ) -> Iterable[Issue]:
        """
        Fetch issues from Jira using JQL with optional filters,
        yielding Issue domain models.
        """
        built_jql = jql or self._build_jql(
            project_keys=project_keys,
            statuses=statuses,
            priorities=priorities,
            assignees=assignees,
            labels=labels,
            text_search=text_search,
        )

        url = f"{self.base_url}/rest/api/3/search/jql"

        fields_list = fields or [
            "summary",
            "status",
            "priority",
            "assignee",
            "labels",
        ]

        payload = {
            "jql": built_jql,
            "fields": fields_list,
            "maxResults": max_results,
        }

        print(url, payload)
        response = requests.post(
            url,
            json=payload,
            auth=self.auth,
            verify=self.verify_ssl,
            timeout=self.timeout,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        print(response.json())

        response.raise_for_status()

        data = response.json()

        for item in data.get("issues", []):
            yield self._to_issue(item)

    def fetch_projects(self) -> List[str]:
        url = f"{self.base_url}/rest/api/3/project/search"
        response = requests.get(
            url,
            auth=self.auth,
            verify=self.verify_ssl,
            timeout=self.timeout,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        data = response.json() or {}
        return [proj.get("key") for proj in data.get("values", []) if proj.get("key")]

    def fetch_statuses(self, project_key: Optional[str] = None) -> List[str]:
        if project_key:
            url = f"{self.base_url}/rest/api/3/project/{project_key}/statuses"
            response = requests.get(
                url,
                auth=self.auth,
                verify=self.verify_ssl,
                timeout=self.timeout,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            data = response.json() or []
            names: List[str] = []
            for wf in data:
                for status in wf.get("statuses", []):
                    name = status.get("name")
                    if name:
                        names.append(name)
            return sorted(set(names))

        url = f"{self.base_url}/rest/api/3/status"
        response = requests.get(
            url,
            auth=self.auth,
            verify=self.verify_ssl,
            timeout=self.timeout,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        data = response.json() or []
        return [s.get("name") for s in data if s.get("name")]

    def fetch_priorities(self) -> List[str]:
        url = f"{self.base_url}/rest/api/3/priority"
        response = requests.get(
            url,
            auth=self.auth,
            verify=self.verify_ssl,
            timeout=self.timeout,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        data = response.json() or []
        return [p.get("name") for p in data if p.get("name")]

    def fetch_assignees(self, query: str = "") -> List[str]:
        url = f"{self.base_url}/rest/api/3/user/search"
        params = {"query": query or ""}
        response = requests.get(
            url,
            params=params,
            auth=self.auth,
            verify=self.verify_ssl,
            timeout=self.timeout,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        data = response.json() or []
        return [u.get("displayName") for u in data if u.get("displayName")]

    def fetch_labels(self, query: str = "") -> List[str]:
        # Jira Cloud supports label search endpoint with optional prefix query
        url = f"{self.base_url}/rest/api/3/label"
        params = {"query": query or ""}
        response = requests.get(
            url,
            params=params,
            auth=self.auth,
            verify=self.verify_ssl,
            timeout=self.timeout,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        data = response.json() or {}
        return [label for label in data.get("values", []) if label]

    def _build_jql(
            self,
            project_keys: Optional[List[str]] = None,
            statuses: Optional[List[str]] = None,
            priorities: Optional[List[str]] = None,
            assignees: Optional[List[str]] = None,
            labels: Optional[List[str]] = None,
            text_search: Optional[str] = None,
    ) -> str:
        conditions: List[str] = []

        if project_keys:
            clean_keys = [k for k in project_keys if k]
            if clean_keys:
                keys = ",".join(clean_keys)
                conditions.append(f"project IN ({keys})")

        if statuses:
            clean = [s for s in statuses if s]
            if clean:
                quoted = ",".join(f'"{s}"' for s in clean)
                conditions.append(f"status IN ({quoted})")

        if priorities:
            clean = [p for p in priorities if p]
            if clean:
                quoted = ",".join(f'"{p}"' for p in clean)
                conditions.append(f"priority IN ({quoted})")

        if assignees:
            clean = [a for a in assignees if a]
            if clean:
                quoted = ",".join(f'"{a}"' for a in clean)
                conditions.append(f"assignee IN ({quoted})")

        if labels:
            clean = [l for l in labels if l]
            if clean:
                quoted = ",".join(f'"{l}"' for l in clean)
                conditions.append(f"labels IN ({quoted})")

        if text_search:
            safe_text = text_search.replace('"', '\\"')
            conditions.append(f'text ~ "{safe_text}"')

        if not conditions:
            conditions.append("updated >= -30d")

        return " AND ".join(conditions) + " ORDER BY updated DESC"

    @staticmethod
    def _to_issue(item: dict) -> Issue:
        fields = item.get("fields", {})

        priority_name = (fields.get("priority") or {}).get("name") or "Medium"
        status_name = (fields.get("status") or {}).get("name") or "Unknown"
        assignee = (fields.get("assignee") or {}).get("displayName")

        is_blocker = (
                priority_name.lower() in {"blocker", "critical"}
                or status_name.lower() == "blocked"
        )

        return Issue(
            id=item.get("key") or str(item.get("id")),
            title=fields.get("summary") or "",
            status=status_name,
            priority=priority_name,
            assignee=assignee,
            is_blocker=is_blocker,
        )
