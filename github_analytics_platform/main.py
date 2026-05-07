from __future__ import annotations

from dataclasses import asdict

from .github_client import GitHubClient
from .metrics import compute_repository_metrics
from .ml import RepositoryHealthModel
from .models import AnalysisResult, RepositorySnapshot
from .recommendations import build_recommendations
from .sample_data import build_sample_snapshot


def analyze_snapshot(snapshot: RepositorySnapshot) -> AnalysisResult:
    metrics = compute_repository_metrics(snapshot)
    model = RepositoryHealthModel()
    prediction = model.predict(metrics)
    recommendations = build_recommendations(metrics, prediction)
    return AnalysisResult(
        repository=snapshot.full_name,
        metrics=metrics,
        predictions=asdict(prediction),
        recommendations=recommendations,
    )


def run_analysis(owner: str | None = None, repo: str | None = None, token: str | None = None) -> AnalysisResult:
    if owner and repo:
        client = GitHubClient(token=token)
        snapshot = client.fetch_repository_snapshot(owner=owner, repo=repo)
    else:
        snapshot = build_sample_snapshot()
    return analyze_snapshot(snapshot)
