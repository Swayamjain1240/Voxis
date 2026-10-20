import numpy as np
import pytest

from src.evaluation.report import build_evaluation_report, held_out_signer_metrics


def test_report_contains_calibration_confusion_and_signer_metrics():
    report = build_evaluation_report(
        [0, 1, 0, 1],
        [0, 1, 1, 1],
        [[0.9, 0.1], [0.2, 0.8], [0.6, 0.4], [0.1, 0.9]],
        labels=["NO", "YES"],
        signer_ids=["s2", "s2", "s3", "s3"],
        test_signers=["s3", "s2"],
        metadata={
            "model_version": "sign-transformer-0.1.0",
            "vocabulary_version": "1.0.0",
            "preprocessing_version": "1.0.0",
        },
    )
    assert report["test_signers"] == ["s2", "s3"]
    assert report["confusion_matrix"] == [[1, 0], [1, 2]]
    assert report["signer_metrics"]["s3"]["num_samples"] == 2
    assert "expected_calibration_error" in report["metrics"]
    assert report["model_version"] == "sign-transformer-0.1.0"


def test_signer_metric_inputs_must_align():
    with pytest.raises(ValueError, match="equal lengths"):
        held_out_signer_metrics([0], [0, 1], ["s1"])
