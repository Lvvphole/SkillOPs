"""Build a pull-request payload (title, body, head, base) for the operator's tooling.

This function does not call any remote API and embeds no credentials. It returns
the structured PR request; the operator's GitHub integration opens the PR and
records the resulting URL in artifacts/pr-url.txt.
"""
from __future__ import annotations

from typing import Dict


def create_pull_request(
    *,
    title: str,
    body: str,
    head: str,
    base: str = "main",
) -> Dict[str, str]:
    if head == base:
        raise ValueError("head and base must differ")
    return {
        "title": title,
        "body": body,
        "head": head,
        "base": base,
    }
