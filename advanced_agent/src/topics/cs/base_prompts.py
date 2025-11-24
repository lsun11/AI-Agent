# src/topics/base_prompts.py
from __future__ import annotations
from abc import ABC


class BaseCSResearchPrompts(ABC):
    """
    Base prompt class for computer-science-related product/tool research.

    This is intended to be reused for:
      - developer tools
      - SaaS products
      - APIs / platforms
      - cloud services, etc.

    Subclasses customize wording by overriding the class attributes:
      - TOPIC_LABEL
      - ANALYSIS_SUBJECT
      - RECOMMENDER_ROLE
    """

    # 🔥 Shared, public, inherited description string
    DESCRIPTION = """
    This prompt class inherits the generic structure from BaseCSResearchPrompts.
    It exposes a consistent interface:

      - TOOL_EXTRACTION_SYSTEM
      - tool_extraction_user(query, content)
      - TOOL_ANALYSIS_SYSTEM
      - tool_analysis_user(company_name, content)
      - RECOMMENDATIONS_SYSTEM
      - recommendations_user(query, company_data)

    All prompt subclasses keep the SAME attribute/method names,
    so your workflow code can call:

        self.prompts.TOOL_EXTRACTION_SYSTEM
        self.prompts.tool_extraction_user(...)
        self.prompts.TOOL_ANALYSIS_SYSTEM
        self.prompts.tool_analysis_user(...)
        self.prompts.RECOMMENDATIONS_SYSTEM
        self.prompts.recommendations_user(...)

    …without needing any modifications when the topic changes.
    """

    # High-level labels that subclasses can override.
    TOPIC_LABEL: str = "technical product, tool, platform, or service"
    ANALYSIS_SUBJECT: str = "technical products and computing technologies"
    RECOMMENDER_ROLE: str = "senior technical advisor"

    # -----------------------------
    # 1) TOOL EXTRACTION PROMPTS
    # -----------------------------
    @property
    def TOOL_EXTRACTION_SYSTEM(self) -> str:
        """
        System message: how the model should behave when extracting tools.
        """
        return (
            f"You are a tech researcher. Extract specific {self.TOPIC_LABEL} names from articles.\n"
            "Focus on actual products/tools that people can use, not general concepts or features."
        )

    @classmethod
    def tool_extraction_user(cls, query: str, content: str) -> str:
        """
        User message template for extraction.

        NOTE: kept the same name/signature as your original,
        but made it generic so subclasses only override class attributes.
        """
        return (
            f"Query: {query}\n"
            f"Article Content: {content}\n\n"
            f'Extract a list of specific {cls.TOPIC_LABEL} names mentioned in this content '
            f'that are relevant to "{query}".\n\n'
            "Rules:\n"
            "- Only include actual product/tool names, not generic terms\n"
            "- Focus on things people can directly use/implement (not just concepts)\n"
            "- Include both open source and commercial options\n"
            "- Limit to the 5 most relevant items\n"
            "- Return just the names, one per line, no descriptions\n\n"
            "Example format:\n"
            "Supabase\n"
            "PlanetScale\n"
            "Railway\n"
            "Appwrite\n"
            "Nhost"
        )

    # -----------------------------
    # 2) TOOL / COMPANY ANALYSIS
    # -----------------------------
    @property
    def TOOL_ANALYSIS_SYSTEM(self) -> str:
        """
        System message: how the model should behave when analyzing a product/tool.
        """
        return (
            f"You are analyzing {self.ANALYSIS_SUBJECT}.\n"
            "Focus on extracting information relevant to programmers and software developers.\n"
            "Pay special attention to programming languages, frameworks, APIs, SDKs, and workflows."
        )

    @classmethod
    def tool_analysis_user(cls, company_name: str, content: str) -> str:
        """
        User message template for tool/company analysis.

        Still uses the same output fields you already rely on
        so it works for dev tools, SaaS, APIs, etc.
        """
        snippet = content[:2500]
        return (
            f"Company/Tool: {company_name}\n"
            f"Website Content: {snippet}\n\n"
            "Analyze this content from a developer's perspective and provide:\n"
            '- pricing_model: One of "Free", "Freemium", "Paid", "Enterprise", or "Unknown".\n'
            '- pricing_details: String with any price information if available (e.g. "from $20/month for Pro", "Free tier + $10/user/month", or null/empty if unclear).\n'
            "- is_open_source: true if open source, false if proprietary, null if unclear\n"
            "- tech_stack: List of programming languages, frameworks, databases, APIs, or technologies supported/used\n"
            "- description: Brief 1-sentence description focusing on what this does for developers\n"
            "- api_available: true if REST API, GraphQL, SDK, or programmatic access is mentioned\n"
            "- language_support: List of programming languages explicitly supported (e.g., Python, JavaScript, Go)\n"
            "- integration_capabilities: List of tools/platforms it integrates with (e.g., GitHub, VS Code, Docker, AWS)\n\n"
            "Focus on developer-relevant features like APIs, SDKs, language support, integrations, "
            "and development workflows."
        )

    # -----------------------------
    # 3) RECOMMENDATION PROMPTS
    # -----------------------------
    @property
    def RECOMMENDATIONS_SYSTEM(self) -> str:
        """
        System message: how the model should behave when giving recommendations.
        """
        return (
            f"You are a {self.RECOMMENDER_ROLE} providing quick, concise tech recommendations.\n"
            "Keep responses brief and actionable - maximum 3-4 sentences total."
        )

    @classmethod
    def recommendations_user(cls, query: str, company_data: str) -> str:
        """
        User message template for final recommendations.
        """
        return (
            f"Developer Query: {query}\n"
            f"Tools/Technologies Analyzed: {company_data}\n\n"
            "Provide a brief recommendation (3-4 sentences max) covering:\n"
            "- Which option is best and why\n"
            "- Key cost/pricing consideration\n"
            "- Main technical advantage\n\n"
            "Be concise and direct - no long explanations needed."
        )
