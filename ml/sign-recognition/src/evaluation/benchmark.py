from __future__ import annotations

from collections.abc import Mapping


def compare_to_baseline(
    model_report: Mapping[str, object],
    baseline_report: Mapping[str, object],
    *,
    metric: str = "balanced_accuracy",
) -> dict[str, object]:
    model_metrics = model_report.get("metrics")
    baseline_metrics = baseline_report.get("metrics")
    if not isinstance(model_metrics, Mapping) or not isinstance(baseline_metrics, Mapping):
        raise ValueError("Both reports must contain a metrics object.")
    model_score = model_metrics.get(metric)
    baseline_score = baseline_metrics.get(metric)
    if not isinstance(model_score, (int, float)) or not isinstance(baseline_score, (int, float)):
        raise ValueError(f"Reports must contain numeric {metric} scores.")
    return {
        "metric": metric,
        "model_score": float(model_score),
        "baseline_score": float(baseline_score),
        "delta": float(model_score - baseline_score),
        "beats_baseline": bool(model_score > baseline_score),
    }
