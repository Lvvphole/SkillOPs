"""Analysis: corrective diagnosis plus preventive/optimization scans.

Passing thresholds do NOT stop improvement. On a pass the loop still runs
staleness, drift, challenge-benchmark, and optimization scans to decide whether
an evidence-backed candidate exists.
"""
from skillops.analysis.analyze_performance import analyze_performance
from skillops.analysis.diagnose_failure import diagnose_failure
from skillops.analysis.run_staleness_check import run_staleness_check
from skillops.analysis.run_drift_check import run_drift_check
from skillops.analysis.run_optimization_scan import run_optimization_scan
from skillops.analysis.run_challenge_benchmarks import run_challenge_benchmarks

__all__ = [
    "analyze_performance",
    "diagnose_failure",
    "run_staleness_check",
    "run_drift_check",
    "run_optimization_scan",
    "run_challenge_benchmarks",
]
