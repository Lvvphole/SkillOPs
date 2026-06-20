"""Recommendations: patch (corrective) and candidate (optimization) suggestions.

Recommendations are the ONLY place LLM-style suggestion is permitted, and even
here the content is constrained: a recommendation may propose a patch or a
candidate, but it may never assert pass/fail. All recommendations must be
verified before they are used.
"""
from skillops.recommendations.recommend_patch import recommend_patch
from skillops.recommendations.recommend_candidate import recommend_candidate
from skillops.recommendations.constrain_recommendation import constrain_recommendation

__all__ = ["recommend_patch", "recommend_candidate", "constrain_recommendation"]
