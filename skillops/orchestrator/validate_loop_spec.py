"""Validate manifests against JSON Schema using a dependency-free validator.

The validator supports the JSON Schema subset used by SkillOps manifests:
type, required, properties, items, enum, minimum, maximum, minItems, oneOf,
and additionalProperties=false. This keeps the runtime dependency-light (PyYAML
only) while still enforcing the schema contract.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

_TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
}


def _check_type(value: Any, expected: str, path: str, errors: List[str]) -> bool:
    if expected == "number" and isinstance(value, bool):
        errors.append(f"{path}: expected number, got boolean")
        return False
    if expected == "integer" and isinstance(value, bool):
        errors.append(f"{path}: expected integer, got boolean")
        return False
    py = _TYPE_MAP.get(expected)
    if py and not isinstance(value, py):
        errors.append(f"{path}: expected {expected}, got {type(value).__name__}")
        return False
    return True


def validate_against_schema(data: Any, schema: Dict[str, Any], path: str = "$") -> List[str]:
    errors: List[str] = []

    if "oneOf" in schema:
        if not any(not validate_against_schema(data, s, path) for s in schema["oneOf"]):
            errors.append(f"{path}: does not match any schema in oneOf")
        return errors

    expected_type = schema.get("type")
    if expected_type and not _check_type(data, expected_type, path, errors):
        return errors

    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{path}: {data!r} not in enum {schema['enum']}")

    if isinstance(data, (int, float)) and not isinstance(data, bool):
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(f"{path}: {data} < minimum {schema['minimum']}")
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(f"{path}: {data} > maximum {schema['maximum']}")

    if isinstance(data, dict):
        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"{path}: missing required property '{key}'")
        props = schema.get("properties", {})
        for key, value in data.items():
            if key in props:
                errors.extend(validate_against_schema(value, props[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False and not key.startswith("_"):
                errors.append(f"{path}: additional property '{key}' not allowed")

    if isinstance(data, list):
        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append(f"{path}: array shorter than minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(data):
                errors.extend(validate_against_schema(item, item_schema, f"{path}[{i}]"))

    return errors


def load_schema(name: str, schemas_root: str = "loops/schemas") -> Dict[str, Any]:
    return json.loads((Path(schemas_root) / name).read_text(encoding="utf-8"))


def validate_loop_spec(
    spec: Dict[str, Any],
    *,
    schema_name: str = "loop-spec.schema.json",
    schemas_root: str = "loops/schemas",
) -> Dict[str, Any]:
    schema = load_schema(schema_name, schemas_root)
    errors = validate_against_schema(spec, schema)
    return {"valid": len(errors) == 0, "errors": errors}
