"""Structured JSON logger. Mirrors src/utils/logger.ts."""
from __future__ import annotations

import json
import os
import sys
from typing import Any

_LEVELS = {"debug": 10, "info": 20, "warn": 30, "error": 40}


class _Logger:
    """Structured logger. All telemetry goes to stderr so stdout stays reserved
    for clean command output (e.g. the JSON loop report from `skillops run`)."""

    def _emit(self, level: str, message: str, meta: Any = None) -> None:
        threshold = _LEVELS.get(os.environ.get("SKILLOPS_LOG_LEVEL", "info"), 20)
        if _LEVELS.get(level, 20) < threshold:
            return
        record = {"level": level, "message": message}
        if meta is not None:
            record["meta"] = meta
        print(json.dumps(record, default=str), file=sys.stderr)

    def debug(self, message: str, meta: Any = None) -> None:
        self._emit("debug", message, meta)

    def info(self, message: str, meta: Any = None) -> None:
        self._emit("info", message, meta)

    def warn(self, message: str, meta: Any = None) -> None:
        self._emit("warn", message, meta)

    def error(self, message: str, meta: Any = None) -> None:
        self._emit("error", message, meta)


logger = _Logger()
