"""Date helpers. Mirrors src/utils/dates.ts (ISO timestamps + ISO week ids)."""
from __future__ import annotations

from datetime import datetime, timezone, date


def now_iso() -> str:
    """UTC timestamp in ISO-8601 with a trailing Z, matching the TS adapter."""
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


def week_id(when: date | datetime | None = None) -> str:
    """ISO week id like '2026-W25'."""
    if when is None:
        when = datetime.now(timezone.utc)
    if isinstance(when, datetime):
        when = when.date()
    iso_year, iso_week, _ = when.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def days_between(earlier_iso: str, later_iso: str) -> float:
    """Whole/fractional days between two ISO timestamps (later - earlier)."""
    a = _parse(earlier_iso)
    b = _parse(later_iso)
    return (b - a).total_seconds() / 86400.0


def _parse(value: str) -> datetime:
    cleaned = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(cleaned)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt
