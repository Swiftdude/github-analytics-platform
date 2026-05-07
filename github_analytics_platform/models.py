from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class CommitRecord:
    sha: str
    author: str
    authored_at: datetime
    additions: int = 0
    deletions: int = 0
    changed_files: int = 0
    touched_files: list[str] = field(default_factory=list)
    message: str = ""

    @property
    def churn(self) -> int:
        return self.additions + self.deletions


@dataclass(slots=True)
class IssueRecord:
    created_at: datetime
    closed_at: datetime | None

    @property
    def resolution_hours(self) -> float | None:
        if self.closed_at is None:
            return None
        delta = self.closed_at - self.created_at
        return delta.total_seconds() / 3600


@dataclass(slots=True)
class RepositorySnapshot:
    owner: str
    name: str
    stars: int
    forks: int
    open_issues: int
    watchers: int
    primary_language: str | None
    languages: dict[str, int]
    commits: list[CommitRecord]
    issues: list[IssueRecord]

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.name}"


@dataclass(slots=True)
class AnalysisResult:
    repository: str
    metrics: dict[str, float | int | str | list[str] | dict[str, float]]
    predictions: dict[str, float | str]
    recommendations: list[str]
