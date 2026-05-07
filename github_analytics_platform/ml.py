from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import RandomForestClassifier


@dataclass(slots=True)
class PredictionResult:
    inactivity_risk: float
    maintainability_score: float
    predicted_status: str


class RepositoryHealthModel:
    def __init__(self) -> None:
        self.model = RandomForestClassifier(n_estimators=120, random_state=42)
        self.feature_names = [
            "commit_frequency_per_day",
            "contributors",
            "bus_factor",
            "commit_entropy",
            "avg_issue_resolution_hours",
            "avg_commit_churn",
            "churn_volatility",
            "open_issues",
            "stars",
        ]
        self._train_on_bootstrap_data()

    def predict(self, metrics: dict[str, float | int | str | list[str] | dict[str, float]]) -> PredictionResult:
        vector = np.array([[float(metrics.get(name, 0.0)) for name in self.feature_names]])
        inactive_probability = float(self.model.predict_proba(vector)[0][1])

        maintainability_score = 100.0
        maintainability_score -= min(float(metrics.get("avg_issue_resolution_hours", 0.0)) / 4.0, 20.0)
        maintainability_score -= min(float(metrics.get("avg_commit_churn", 0.0)) / 15.0, 20.0)
        maintainability_score -= min(float(metrics.get("open_issues", 0.0)) * 1.5, 15.0)
        maintainability_score += min(float(metrics.get("contributors", 0.0)) * 3.0, 12.0)
        maintainability_score += min(float(metrics.get("commit_entropy", 0.0)) * 4.0, 8.0)
        maintainability_score += min(float(metrics.get("bus_factor", 0.0)) * 2.0, 10.0)
        maintainability_score += min(float(metrics.get("commit_frequency_per_day", 0.0)) * 25.0, 10.0)
        maintainability_score = max(0.0, min(100.0, maintainability_score))

        if inactive_probability >= 0.65:
            predicted_status = "at_risk"
        elif maintainability_score >= 75:
            predicted_status = "healthy"
        else:
            predicted_status = "needs_attention"

        return PredictionResult(
            inactivity_risk=round(inactive_probability, 3),
            maintainability_score=round(maintainability_score, 2),
            predicted_status=predicted_status,
        )

    def _train_on_bootstrap_data(self) -> None:
        data = np.array(
            [
                [0.40, 8, 4, 2.4, 18, 42, 20, 8, 1500],
                [0.22, 5, 3, 1.9, 24, 60, 35, 12, 420],
                [0.10, 3, 2, 1.1, 72, 95, 80, 30, 120],
                [0.03, 1, 1, 0.0, 0, 160, 120, 40, 12],
                [0.70, 12, 6, 2.8, 8, 35, 18, 4, 8200],
                [0.18, 4, 2, 1.5, 32, 84, 55, 18, 275],
                [0.01, 1, 1, 0.0, 120, 210, 150, 48, 4],
                [0.33, 6, 3, 1.7, 20, 50, 28, 9, 900],
                [0.08, 2, 1, 0.9, 60, 130, 95, 22, 65],
                [0.52, 9, 5, 2.2, 14, 40, 24, 6, 2100],
            ]
        )
        labels = np.array([0, 0, 1, 1, 0, 1, 1, 0, 1, 0])
        self.model.fit(data, labels)
