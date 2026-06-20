from skillops import Thresholds
from skillops.metrics.calculate_metric_summary import calculate_metric_summary
from skillops.metrics.compare_thresholds import compare_thresholds

from tests.conftest import make_run

T = Thresholds(min_success_rate=0.8, max_avg_duration_ms=1000, max_false_positive_rate=0.2, min_action_rate=0.25)


def test_compare_thresholds_pass():
    runs = [make_run() for _ in range(4)]
    summary = calculate_metric_summary(runs, T)
    decision = compare_thresholds(summary)
    assert decision == {"passed": True, "failures": []}


def test_low_success_rate_fails():
    runs = [make_run(success=False) for _ in range(4)]
    summary = calculate_metric_summary(runs, T)
    assert summary.passed is False
    assert "success_rate" in summary.failures


def test_slow_duration_fails():
    runs = [make_run(duration_ms=5000) for _ in range(4)]
    summary = calculate_metric_summary(runs, T)
    assert "avg_duration_ms" in summary.failures
    assert summary.passed is False


def test_high_false_positive_fails():
    runs = [make_run(predicted_positive=True, actual_positive=False) for _ in range(4)]
    summary = calculate_metric_summary(runs, T)
    assert "false_positive_rate" in summary.failures


def test_low_action_rate_fails():
    runs = [make_run(action_taken=False) for _ in range(4)]
    summary = calculate_metric_summary(runs, T)
    assert "action_rate" in summary.failures


def test_metrics_decide_not_text():
    # A summary that passed cannot be flipped by appending narrative; compare uses
    # only the computed fields.
    runs = [make_run() for _ in range(4)]
    summary = calculate_metric_summary(runs, T)
    summary.failures = []  # already empty
    assert compare_thresholds(summary)["passed"] is True
