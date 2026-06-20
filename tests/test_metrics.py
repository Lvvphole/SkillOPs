from skillops import Thresholds
from skillops.metrics.calculate_success_rate import calculate_success_rate
from skillops.metrics.calculate_avg_duration import calculate_avg_duration
from skillops.metrics.calculate_false_positive_rate import calculate_false_positive_rate
from skillops.metrics.calculate_action_rate import calculate_action_rate
from skillops.metrics.calculate_metric_summary import calculate_metric_summary

from tests.conftest import make_run


def test_success_rate():
    runs = [make_run(success=True), make_run(success=False)]
    assert calculate_success_rate(runs) == 0.5
    assert calculate_success_rate([]) == 0.0


def test_avg_duration():
    runs = [make_run(duration_ms=10), make_run(duration_ms=20)]
    assert calculate_avg_duration(runs) == 15
    assert calculate_avg_duration([]) == 0.0


def test_false_positive_rate():
    runs = [
        make_run(predicted_positive=True, actual_positive=False),  # FP
        make_run(predicted_positive=True, actual_positive=True),
        make_run(predicted_positive=False, actual_positive=False),
    ]
    assert calculate_false_positive_rate(runs) == 0.5
    # no predicted positives -> 0
    assert calculate_false_positive_rate([make_run(predicted_positive=False)]) == 0.0


def test_action_rate():
    runs = [make_run(action_taken=True), make_run(action_taken=False), make_run(action_taken=False)]
    assert round(calculate_action_rate(runs), 4) == 0.3333


def test_metric_summary_passes_clean_sample():
    runs = [make_run() for _ in range(4)]
    t = Thresholds(0.8, 1000, 0.2, 0.25)
    summary = calculate_metric_summary(runs, t)
    assert summary.passed is True
    assert summary.failures == []
    assert summary.sample_size == 4
