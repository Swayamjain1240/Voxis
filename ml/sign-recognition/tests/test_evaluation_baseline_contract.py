import numpy as np

from src.evaluation.benchmark import compare_to_baseline
from src.evaluation.report import build_evaluation_report
from src.models.baseline import TemporalCentroidClassifier


def test_baseline_can_be_reported_and_compared_on_a_signer_split():
    train = np.zeros((4, 60, 300), dtype=np.float64)
    train[:2] += 1
    train[2:] -= 1
    test = np.zeros((2, 60, 300), dtype=np.float64)
    test[0] += 1
    test[1] -= 1
    baseline = TemporalCentroidClassifier(num_classes=2).fit(train, [0, 0, 1, 1])
    report = build_evaluation_report(
        baseline.predict(test),
        [0, 1],
        baseline.predict_proba(test),
        labels=["NO", "YES"],
        signer_ids=["held-out-a", "held-out-a"],
        test_signers=["held-out-a"],
    )
    comparison = compare_to_baseline(report, report)
    assert report["metrics"]["balanced_accuracy"] == 1.0
    assert comparison["beats_baseline"] is False
