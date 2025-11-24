from typing import List, Optional
from pydantic import BaseModel

from ..base_models import (
    BaseSECompanyAnalysis,
    BaseSECompanyInfo,
    BaseSEResearchState,
)


class TestingCompanyAnalysis(BaseSECompanyAnalysis):
    """Specialized analysis model for testing resources."""

    # extend or override as needed
    domain_specific_notes: Optional[str] = None


class TestingCompanyInfo(BaseSECompanyInfo):
    """Specialized resource info for testing."""

    # example: add a rating or dimension relevant to this subtopic
    relevance_score: Optional[float] = None


class TestingResearchState(BaseSEResearchState):
    """State for testing research workflows."""

    # Keep base fields; can add more later if needed.
    pass
