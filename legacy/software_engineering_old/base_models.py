from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class BaseSECompanyAnalysis(BaseModel):
    """Generic structured analysis for a software engineering resource.

    This is intentionally broad and can be extended by subtopics.
    """

    primary_focus: str = ""  # e.g. testing, architecture, productivity
    difficulty_level: Optional[str] = None  # Beginner, Intermediate, Advanced
    ideal_audience: List[str] = []  # e.g. Backend devs, SREs, Team leads
    key_practices: List[str] = []  # e.g. TDD, code review, CI/CD
    benefits: List[str] = []       # e.g. fewer bugs, faster releases
    drawbacks: List[str] = []      # tradeoffs, limitations
    recommended_usage: str = ""    # brief guidance text


class BaseSECompanyInfo(BaseModel):
    """Generic 'resource' / 'tool' info for software engineering topics.

    Not necessarily a 'company' - could be a book, tool, platform, or guide.
    """

    name: str
    description: str
    website: str
    category: Optional[str] = None  # e.g. IDE, CI tool, testing framework
    tags: List[str] = []
    pricing_model: Optional[str] = None
    pricing_details: Optional[str] = None
    # Domain-agnostic metadata
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    competitors: List[str] = []


class BaseSEResearchState(BaseModel):
    """Shared research state for software engineering workflows."""

    query: str
    extracted_resources: List[str] = []  # tools/books/platforms extracted
    resources: List[BaseSECompanyInfo] = []
    search_results: List[Dict[str, Any]] = []
    analysis: Optional[str] = None
