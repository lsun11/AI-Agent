# src/topics/tools/base_prompts.py

from __future__ import annotations

from abc import ABC
from typing import ClassVar


class BaseCSResearchPrompts(ABC):
    """
    Base prompt class for tool/software/service recommendation across CS topics.

    Examples of supported queries:
      - "Best hosted Postgres for small startup?"
      - "Alternatives to Datadog for infra monitoring"
      - "Tools for system design interview practice"
      - "API gateways for microservices on Kubernetes"

    The workflow still uses a 3-stage pattern:

      1) TOOL_EXTRACTION_SYSTEM + tool_extraction_user
         → find candidate tools/services/platforms

      2) TOOL_ANALYSIS_SYSTEM + tool_analysis_user
         → structured per-tool analysis (pricing, pros/cons, fit, etc.)

      3) RECOMMENDATIONS_SYSTEM + recommendations_user
         → comparison + final recommendation and decision guide
    """

    # High-level labels that subclasses can override.
    TOPIC_LABEL: ClassVar[str] = (
        "technology product, tool, service, platform, or API"
    )
    ANALYSIS_SUBJECT: ClassVar[str] = (
        "software tools, hosted services, APIs, platforms, and related products"
    )
    RECOMMENDER_ROLE: ClassVar[str] = "senior staff engineer and tooling advisor"

    # -----------------------------
    # 1) TOOL EXTRACTION PROMPTS
    # -----------------------------
    @property
    def TOOL_EXTRACTION_SYSTEM(self) -> str:
        """
        System message: how the model should behave when extracting tools.
        """
        return (
            f"You are a technology research assistant. Extract specific {self.TOPIC_LABEL} "
            "names from articles, docs, or websites.\n"
            "You should handle *any* CS-related topic: developer tools, cloud services, "
            "monitoring, CI/CD, security tools, learning platforms, career platforms "
            "viewed as products, etc.\n"
            "Focus ONLY on concrete tools/services people can actually use, install, "
            "subscribe to, or sign up for."
        )

    @classmethod
    def tool_extraction_user(cls, query: str, content: str) -> str:
        """
        User message template for extraction.
        """
        return (
            f"User Query: {query}\n"
            f"Source Content:\n{content}\n\n"
            f"Task: Extract a list of specific {cls.TOPIC_LABEL} names mentioned in this content "
            f"that are relevant to the query.\n\n"
            "Rules:\n"
            "- Only include actual product/tool/service names, not generic concepts\n"
            "- Include dev tools, hosted SaaS, APIs, infra services, monitoring, learning platforms, etc.\n"
            "- Focus on things people can directly use (install, call via API, subscribe to, etc.)\n"
            "- Limit to the 5–10 most relevant items\n"
            "- Return just the names, one per line, no descriptions and no numbering\n"
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
            "You must produce a *structured JSON object* that can be parsed by code, "
            "matching the BaseCompanyAnalysis schema.\n"
            "Think from the perspective of professional developers and engineering teams."
        )

    @classmethod
    def tool_analysis_user(cls, company_name: str, content: str) -> str:
        """
        User message template for tool/company analysis.

        Output must match BaseCompanyAnalysis:
          - pricing_model (Free, Freemium, Paid, Enterprise, Unknown)
          - pricing_details
          - is_open_source
          - category
          - primary_use_case
          - target_users
          - tech_stack
          - description
          - api_available
          - language_support
          - integration_capabilities
          - strengths
          - limitations
          - ideal_for
          - not_suited_for
        """
        snippet = content[:2500]
        return (
            f"Tool / Service / Platform: {company_name}\n"
            f"Website or Documentation Content (truncated):\n{snippet}\n\n"
            "Analyze this from a developer/engineering perspective and return "
            "a single JSON object with the following fields:\n"
            '- pricing_model: One of "Free", "Freemium", "Paid", "Enterprise", or "Unknown".\n'
            '- pricing_details: Short string with any price info if available (e.g. '
            '"from $20/month", "Free tier + $10/user/month"), or null/empty if unclear.\n'
            "- is_open_source: true if clearly open source, false if clearly proprietary, null if unclear.\n"
            '- category: Short description of the category (e.g. "Cloud database", "CI/CD platform").\n'
            '- primary_use_case: Short phrase summarizing the main use case.\n'
            '- target_users: Array of user types (e.g. [\"Backend engineers\", \"Data teams\"]).\n'
            "- tech_stack: Array of notable languages, frameworks, infra, or technologies.\n"
            "- description: 1-sentence description of what it does for developers.\n"
            "- api_available: true if API/SDK/programmatic access is mentioned; false if clearly none; null if unclear.\n"
            "- language_support: Array of supported programming languages if applicable.\n"
            "- integration_capabilities: Array of integrations (e.g. GitHub, VS Code, AWS, Slack).\n"
            "- strengths: Array of concrete strengths or advantages.\n"
            "- limitations: Array of concrete downsides or gaps.\n"
            "- ideal_for: Array of scenarios or team types where this is a strong fit.\n"
            "- not_suited_for: Array of scenarios where this is likely a bad fit.\n\n"
            "Return ONLY a valid JSON object, no extra commentary."
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
            f"You are a {self.RECOMMENDER_ROLE} comparing multiple tools/services.\n"
            "Your job is to produce a concise but *structured* comparison that can drive "
            "a product choice.\n"
            "You must return JSON compatible with the ToolComparisonRecommendation model."
        )

    @classmethod
    def recommendations_user(cls, query: str, company_data: str) -> str:
        """
        User message template for final recommendations.

        `company_data` is a JSON array of BaseCompanyInfo-like objects.
        """
        return (
            f"User Query: {query}\n"
            f"Candidate tools/services (JSON array):\n{company_data}\n\n"
            "Using this data, produce a JSON object with fields:\n"
            "- primary_choice: name of the single best option for this query (or null if unclear).\n"
            "- backup_options: array of 1–3 reasonable alternatives.\n"
            "- summary: 2–4 sentence plain-text summary comparing the main options.\n"
            "- selection_criteria: bullet-style array of criteria that matter most (e.g. budget, scale, simplicity).\n"
            "- tradeoffs: array describing key tradeoffs between the top options.\n"
            "- step_by_step_decision_guide: array of 3–7 concrete steps the user can follow to decide.\n\n"
            "Return ONLY a valid JSON object. No extra commentary, no markdown."
        )
