"""PR automation: branch creation, diff capture, PR payload, and summary writing.

These utilities build the evidence and payload for a pull request. Actual remote
PR creation is performed by the operator's GitHub tooling using the payload from
create_pull_request(); the runtime never embeds credentials.
"""
from skillops.pr.create_branch import create_branch, current_branch
from skillops.pr.capture_diff import capture_diff
from skillops.pr.create_pull_request import create_pull_request
from skillops.pr.write_pr_summary import write_pr_summary

__all__ = [
    "create_branch",
    "current_branch",
    "capture_diff",
    "create_pull_request",
    "write_pr_summary",
]
