"""Numeric averaging helper. Mirrors src/utils/average.ts."""
from __future__ import annotations

from typing import Iterable


def average(values: Iterable[float]) -> float:
    """Return the arithmetic mean, or 0.0 for an empty sequence."""
    items = list(values)
    if not items:
        return 0.0
    return sum(items) / len(items)
