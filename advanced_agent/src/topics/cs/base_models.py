# src/topics/base_models.py
from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class BaseCompanyAnalysis(BaseModel):
    """
    Generic structured output for LLM analysis of a product/service/platform.
    Designed to be reused across topics: developer tools, SaaS, APIs, etc.
    """
    # Pricing and licensing
    pricing_model: str  # Free, Freemium, Paid, Enterprise, Unknown
    pricing_details: Optional[str] = None  # <-- NEW: e.g. "from $20/month"
    # Openness / licensing
    is_open_source: Optional[bool] = None

    # Technical aspects
    tech_stack: List[str] = Field(default_factory=list)
    description: str = ""
    api_available: Optional[bool] = None
    language_support: List[str] = Field(default_factory=list)
    integration_capabilities: List[str] = Field(default_factory=list)


class BaseCompanyInfo(BaseModel):
    """
    Generic representation of a company/tool/service being researched.
    This base is intentionally broad enough to cover dev tools, SaaS, APIs, etc.
    """
    name: str
    description: str
    website: str

    # Business / licensing
    pricing_model: Optional[str] = None
    pricing_details: Optional[str] = None
    is_open_source: Optional[bool] = None

    # Technical aspects
    tech_stack: List[str] = Field(default_factory=list)
    competitors: List[str] = Field(default_factory=list)
    api_available: Optional[bool] = None
    language_support: List[str] = Field(default_factory=list)
    integration_capabilities: List[str] = Field(default_factory=list)


class BaseResearchState(BaseModel):
    """
    Shared runtime state for any 'product research' workflow.

    Field names are intentionally kept compatible with your original
    developer tools state so they can be reused easily across topics.
    """
    # Original query
    query: str

    # Names extracted from search/scraped content
    extracted_tools: List[str] = Field(default_factory=list)

    # Structured info about the entities we are analyzing
    companies: List[BaseCompanyInfo] = Field(default_factory=list)

    # Raw search results or intermediate info
    search_results: List[Dict[str, Any]] = Field(default_factory=list)

    # Final overall analysis / recommendation text
    analysis: Optional[str] = None

    log_messages: List[str] = []