from typing import List, Optional
from pydantic import BaseModel

from ..base_models import (
    BaseSECompanyAnalysis,
    BaseSECompanyInfo,
    BaseSEResearchState,
)


class ProductivityCompanyAnalysis(BaseSECompanyAnalysis):
    """Specialized analysis model for productivity resources."""

    # extend or override as needed
    domain_specific_notes: Optional[str] = None


class ProductivityCompanyInfo(BaseSECompanyInfo):
    """Specialized resource info for productivity."""

    # example: add a rating or dimension relevant to this subtopic
    relevance_score: Optional[float] = None


class ProductivityResearchState(BaseSEResearchState):
    """State for productivity research workflows."""

    # Keep base fields; can add more later if needed.
    pass
