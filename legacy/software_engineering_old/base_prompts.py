from abc import ABC, abstractmethod


class BaseSEPrompts(ABC):
    """Base prompt set for Software Engineering topics.

    Subtopics (code quality, testing, architecture, etc.) should subclass this
    and customize the SYSTEM texts + user prompt templates.
    """

    # Tool / resource extraction
    TOOL_EXTRACTION_SYSTEM: str = (
        "You are an experienced software engineer and researcher. "
        "From the following content, extract specific tools, frameworks, "
        "platforms, practices, or named resources that engineers can use."
    )

    # Analysis
    TOOL_ANALYSIS_SYSTEM: str = (
        "You are a senior software engineer analyzing tools, frameworks, "
        "and practices for professional developers. Focus on real-world usage, "
        "tradeoffs, and practical guidance."
    )

    # Recommendations
    RECOMMENDATIONS_SYSTEM: str = (
        "You are a staff-level engineer giving concise recommendations. "
        "Keep answers short, practical, and focused on what engineers should do next."
    )

    @abstractmethod
    def tool_extraction_user(self, query: str, content: str) -> str:
        """Build the user message for extracting named tools/resources."""
        raise NotImplementedError

    @abstractmethod
    def tool_analysis_user(self, resource_name: str, content: str) -> str:
        """Build the user message for analyzing a single resource in depth."""
        raise NotImplementedError

    @abstractmethod
    def recommendations_user(self, query: str, resource_data: str) -> str:
        """Build the user message for high-level recommendations."""
        raise NotImplementedError
