from __future__ import annotations

from datetime import datetime
from typing import Any

import requests

from .models import CommitRecord, IssueRecord, RepositorySnapshot


class GitHubClient:
    def __init__(self, token: str | None = None, timeout: int = 20) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "User-Agent": "github-analytics-platform",
            }
        )
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def fetch_repository_snapshot(
        self, owner: str, repo: str, commit_limit: int = 50, issue_limit: int = 30
    ) -> RepositorySnapshot:
        repo_payload = self._get_json(f"https://api.github.com/repos/{owner}/{repo}")
        languages = self._get_json(f"https://api.github.com/repos/{owner}/{repo}/languages")
        commits_payload = self._get_json(
            f"https://api.github.com/repos/{owner}/{repo}/commits?per_page={commit_limit}"
        )
        issues_payload = self._get_json(
            f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page={issue_limit}"
        )

        commits = [self._fetch_commit_detail(owner, repo, commit["sha"]) for commit in commits_payload]
        issues = [self._parse_issue(issue) for issue in issues_payload if "pull_request" not in issue]

        return RepositorySnapshot(
            owner=owner,
            name=repo,
            stars=repo_payload["stargazers_count"],
            forks=repo_payload["forks_count"],
            open_issues=repo_payload["open_issues_count"],
            watchers=repo_payload["subscribers_count"],
            primary_language=repo_payload.get("language"),
            languages=languages,
            commits=commits,
            issues=issues,
        )

    def _fetch_commit_detail(self, owner: str, repo: str, sha: str) -> CommitRecord:
        payload = self._get_json(f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}")
        commit_data = payload["commit"]
        files = payload.get("files", [])
        author = payload.get("author", {}) or {}
        author_name = author.get("login") or commit_data["author"].get("name") or "unknown"
        authored_at = self._parse_datetime(commit_data["author"]["date"])
        return CommitRecord(
            sha=sha,
            author=author_name,
            authored_at=authored_at,
            additions=payload.get("stats", {}).get("additions", 0),
            deletions=payload.get("stats", {}).get("deletions", 0),
            changed_files=len(files),
            touched_files=[file_info["filename"] for file_info in files],
            message=commit_data.get("message", ""),
        )

    def _parse_issue(self, payload: dict[str, Any]) -> IssueRecord:
        return IssueRecord(
            created_at=self._parse_datetime(payload["created_at"]),
            closed_at=self._parse_datetime(payload["closed_at"]) if payload.get("closed_at") else None,
        )

    def _get_json(self, url: str) -> Any:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _parse_datetime(value: str) -> datetime:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
