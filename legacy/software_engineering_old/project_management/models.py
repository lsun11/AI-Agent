from typing import List, Optional
from pydantic import BaseModel

from ..base_models import (
    BaseSECompanyAnalysis,
    BaseSECompanyInfo,
    BaseSEResearchState,
)


class ProjectManagementCompanyAnalysis(BaseSECompanyAnalysis):
    """Specialized analysis model for project management resources."""

    # extend or override as needed
    domain_specific_notes: Optional[str] = None


class ProjectManagementCompanyInfo(BaseSECompanyInfo):
    """Specialized resource info for project management."""

    # example: add a rating or dimension relevant to this subtopic
    relevance_score: Optional[float] = None


class ProjectManagementResearchState(BaseSEResearchState):
    """State for project management research workflows."""

    # Keep base fields; can add more later if needed.
    pass
