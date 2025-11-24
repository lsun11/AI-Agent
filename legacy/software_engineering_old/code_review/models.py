from typing import List, Optional
from pydantic import BaseModel

from ..base_models import (
    BaseSECompanyAnalysis,
    BaseSECompanyInfo,
    BaseSEResearchState,
)


class CodeReviewCompanyAnalysis(BaseSECompanyAnalysis):
    """Specialized analysis model for code review resources."""

    # extend or override as needed
    domain_specific_notes: Optional[str] = None


class CodeReviewCompanyInfo(BaseSECompanyInfo):
    """Specialized resource info for code review."""

    # example: add a rating or dimension relevant to this subtopic
    relevance_score: Optional[float] = None


class CodeReviewResearchState(BaseSEResearchState):
    """State for code review research workflows."""

    # Keep base fields; can add more later if needed.
    pass
