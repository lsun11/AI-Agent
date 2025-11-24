from typing import List, Optional
from pydantic import BaseModel


from ..base_models import (
    BaseSECompanyAnalysis,
    BaseSECompanyInfo,
    BaseSEResearchState,
)


class ArchitectureDesignCompanyAnalysis(BaseSECompanyAnalysis):
    """Specialized analysis model for architecture design resources."""

    # extend or override as needed
    domain_specific_notes: Optional[str] = None


class ArchitectureDesignCompanyInfo(BaseSECompanyInfo):
    """Specialized resource info for architecture design."""

    # example: add a rating or dimension relevant to this subtopic
    relevance_score: Optional[float] = None


class ArchitectureDesignResearchState(BaseSEResearchState):
    """State for architecture design research workflows."""

    # Keep base fields; can add more later if needed.
    pass
