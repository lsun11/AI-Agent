from typing import List, Optional
from pydantic import BaseModel

from ..base_models import (
    BaseSECompanyAnalysis,
    BaseSECompanyInfo,
    BaseSEResearchState,
)


class CodeQualityCompanyAnalysis(BaseSECompanyAnalysis):
    """Specialized analysis model for code quality resources."""

    # extend or override as needed
    domain_specific_notes: Optional[str] = None


class CodeQualityCompanyInfo(BaseSECompanyInfo):
    """Specialized resource info for code quality."""

    # example: add a rating or dimension relevant to this subtopic
    relevance_score: Optional[float] = None


class CodeQualityResearchState(BaseSEResearchState):
    """State for code quality research workflows."""

    # Keep base fields; can add more later if needed.
    pass
