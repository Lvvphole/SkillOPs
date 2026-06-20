# Incident Triage Skill

Classify high-severity or customer-impacting incidents as **urgent**; classify
all others as **standard**. Urgent incidents trigger an action (escalation).

## Decision policy
- `severity == "high"` OR `customer_impact == true` -> `urgent` (action taken)
- otherwise -> `standard` (no action)

## Evaluation
Ground truth is the same predicate (severity high or customer impact). A run is
successful when the predicted label matches ground truth. Metrics derived from
runs (success rate, avg duration, false-positive rate, action rate) decide
pass/fail against the thresholds in `thresholds.yaml`.

This file documents the active behavior; concrete versions live under
`versions/` and are never overwritten without a changelog entry.
