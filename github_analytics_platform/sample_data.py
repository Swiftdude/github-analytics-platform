from __future__ import annotations

from datetime import datetime, timedelta

from .models import CommitRecord, IssueRecord, RepositorySnapshot


def build_sample_snapshot() -> RepositorySnapshot:
    now = datetime.utcnow()
    authors = ["alex", "maya", "alex", "sam", "alex", "maya", "zoe", "alex"]
    churn_values = [120, 55, 32, 180, 75, 12, 25, 8]
    days_ago = [1, 3, 5, 10, 18, 32, 44, 65]
    touched = [
        ["src/api.py", "src/models.py", "README.md"],
        ["src/dashboard.js", "src/charts.js"],
        ["src/api.py"],
        ["src/pipeline.py", "src/metrics.py", "src/ml.py", "src/recommend.py"],
        ["src/pipeline.py", "src/storage.sql"],
        ["docs/setup.md"],
        ["src/metrics.py"],
        ["README.md"],
    ]

    commits: list[CommitRecord] = []
    for index, author in enumerate(authors):
        additions = int(churn_values[index] * 0.65)
        deletions = churn_values[index] - additions
        authored_at = now - timedelta(days=days_ago[index])
        commits.append(
            CommitRecord(
                sha=f"sample-{index}",
                author=author,
                authored_at=authored_at,
                additions=additions,
                deletions=deletions,
                changed_files=len(touched[index]),
                touched_files=touched[index],
                message=f"Sample commit {index}",
            )
        )

    issues = [
        IssueRecord(created_at=now - timedelta(days=14), closed_at=now - timedelta(days=11)),
        IssueRecord(created_at=now - timedelta(days=12), closed_at=now - timedelta(days=8)),
        IssueRecord(created_at=now - timedelta(days=7), closed_at=None),
        IssueRecord(created_at=now - timedelta(days=3), closed_at=now - timedelta(days=1)),
    ]

    return RepositorySnapshot(
        owner="sample",
        name="github-analytics-platform",
        stars=48,
        forks=9,
        open_issues=6,
        watchers=18,
        primary_language="Python",
        languages={"Python": 8200, "JavaScript": 3100, "SQL": 750},
        commits=commits,
        issues=issues,
    )
