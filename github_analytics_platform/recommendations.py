from __future__ import annotations

from .ml import PredictionResult


def build_recommendations(
    metrics: dict[str, float | int | str | list[str] | dict[str, float]],
    prediction: PredictionResult,
) -> list[str]:
    recommendations: list[str] = []

    if float(metrics.get("bus_factor", 0.0)) <= 1:
        recommendations.append("Bus factor is low. Spread ownership across more contributors to reduce delivery risk.")
    if float(metrics.get("commit_frequency_per_day", 0.0)) < 0.08:
        recommendations.append("Recent commit cadence is low. A regular release or maintenance schedule could prevent inactivity.")
    if float(metrics.get("avg_issue_resolution_hours", 0.0)) > 48:
        recommendations.append("Issue resolution is slow. Triage SLAs and smaller scoped issues would likely improve responsiveness.")
    if float(metrics.get("avg_commit_churn", 0.0)) > 100:
        recommendations.append("Average commit churn is high. Smaller pull requests may improve review quality and maintainability.")
    if float(metrics.get("churn_volatility", 0.0)) > 75:
        recommendations.append("Change size is highly volatile. Stabilizing delivery into smaller batches can reduce regression risk.")

    high_churn_files = metrics.get("high_churn_files", [])
    if isinstance(high_churn_files, list) and high_churn_files:
        joined = ", ".join(high_churn_files[:3])
        recommendations.append(f"Most frequently touched files include {joined}. These are good candidates for refactoring or better test coverage.")

    if prediction.predicted_status == "at_risk":
        recommendations.append("This repository is at risk of becoming inactive. Increase contributor depth and keep issue response times short.")
    elif prediction.predicted_status == "healthy":
        recommendations.append("The repository looks healthy. Preserve momentum with contributor onboarding docs and release hygiene.")
    else:
        recommendations.append("The repository is serviceable but fragile in places. Focus on ownership spread and predictable maintenance loops.")

    return recommendations
