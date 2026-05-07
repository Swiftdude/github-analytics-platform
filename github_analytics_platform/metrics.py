from __future__ import annotations

from collections import Counter
from math import log2

import pandas as pd

from .models import RepositorySnapshot


def compute_repository_metrics(snapshot: RepositorySnapshot) -> dict[str, float | int | str | list[str] | dict[str, float]]:
    commit_df = pd.DataFrame(
        [
            {
                "author": commit.author,
                "authored_at": commit.authored_at,
                "additions": commit.additions,
                "deletions": commit.deletions,
                "changed_files": commit.changed_files,
                "churn": commit.churn,
                "touched_files": commit.touched_files,
            }
            for commit in snapshot.commits
        ]
    )
    issue_resolution_hours = [issue.resolution_hours for issue in snapshot.issues if issue.resolution_hours is not None]

    if commit_df.empty:
        return {
            "repository": snapshot.full_name,
            "primary_language": snapshot.primary_language or "Unknown",
            "contributors": 0,
            "total_commits": 0,
            "stars": snapshot.stars,
            "forks": snapshot.forks,
            "avg_issue_resolution_hours": 0.0,
        }

    commit_df["date"] = pd.to_datetime(commit_df["authored_at"])
    commit_df["week"] = commit_df["date"].dt.to_period("W").astype(str)

    contributor_counts = commit_df["author"].value_counts()
    total_commits = int(len(commit_df))
    bus_factor = int((contributor_counts.cumsum() <= total_commits * 0.5).sum() + 1)
    entropy = _commit_entropy(contributor_counts.tolist())
    weekly_counts = commit_df.groupby("week").size()
    file_churn = _top_file_churn(commit_df["touched_files"].tolist())
    normalized_languages = _normalize_language_mix(snapshot.languages)

    recent_days = max((commit_df["date"].max() - commit_df["date"].min()).days, 1)
    commit_frequency = round(total_commits / recent_days, 3)
    avg_churn = round(float(commit_df["churn"].mean()), 2)
    churn_volatility = round(float(commit_df["churn"].std(ddof=0) or 0.0), 2)

    return {
        "repository": snapshot.full_name,
        "primary_language": snapshot.primary_language or "Unknown",
        "contributors": int(contributor_counts.size),
        "total_commits": total_commits,
        "stars": snapshot.stars,
        "forks": snapshot.forks,
        "watchers": snapshot.watchers,
        "open_issues": snapshot.open_issues,
        "commit_frequency_per_day": commit_frequency,
        "avg_commit_churn": avg_churn,
        "churn_volatility": churn_volatility,
        "avg_changed_files": round(float(commit_df["changed_files"].mean()), 2),
        "weekly_activity_std": round(float(weekly_counts.std(ddof=0) or 0.0), 2),
        "bus_factor": bus_factor,
        "commit_entropy": round(entropy, 3),
        "avg_issue_resolution_hours": round(float(pd.Series(issue_resolution_hours).mean() if issue_resolution_hours else 0.0), 2),
        "language_mix": normalized_languages,
        "high_churn_files": file_churn,
    }


def _commit_entropy(commit_counts: list[int]) -> float:
    total = sum(commit_counts)
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in commit_counts:
        probability = count / total
        entropy -= probability * log2(probability)
    return entropy


def _top_file_churn(touched_files: list[list[str]]) -> list[str]:
    counter: Counter[str] = Counter()
    for file_list in touched_files:
        counter.update(file_list)
    return [filename for filename, _ in counter.most_common(5)]


def _normalize_language_mix(languages: dict[str, int]) -> dict[str, float]:
    total = sum(languages.values())
    if total == 0:
        return {}
    return {language: round(value / total, 3) for language, value in languages.items()}
