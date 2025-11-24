from ..base_prompts import BaseSEPrompts


class ProductivityPrompts(BaseSEPrompts):
    """Prompts specialized for the 'productivity' subtopic."""

    TOOL_EXTRACTION_SYSTEM = (
        "You are an expert software engineer focusing on productivity. "
        "From the following content, extract specific tools, frameworks, platforms, "
        "books, or named practices that practitioners can actually adopt."
    )

    TOOL_ANALYSIS_SYSTEM = (
        "You are analyzing productivity resources for professional developers. "
        "Focus on practical usage, strengths, weaknesses, and when to use them."
    )

    RECOMMENDATIONS_SYSTEM = (
        "You are a staff-level engineer advising a team on productivity choices. "
        "Give concise, actionable recommendations in 3-4 sentences."
    )

    def tool_extraction_user(self, query: str, content: str) -> str:
        return (
            f"Query: {query}\n"
            f"Content: {content}\n\n"
            "Extract a list of concrete resources related to this query, such as tools, "
            "frameworks, services, books, or well-known practices.\n"
            "- Only include specific names, not generic concepts.\n"
            "- Focus on items developers can adopt in real projects.\n"
            "- Return just the names, one per line, no descriptions."
        )

    def tool_analysis_user(self, resource_name: str, content: str) -> str:
        return (
            f"Resource: {resource_name}\n"
            f"Website or Documentation Content: {content}\n\n"
            "Analyze this resource from a practical productivity perspective and "
            "fill the BaseSECompanyAnalysis fields. Focus on:\n"
            "- primary_focus: what aspect of software engineering it mainly helps with\n"
            "- difficulty_level: Beginner / Intermediate / Advanced\n"
            "- ideal_audience: who should use it\n"
            "- key_practices: main techniques or practices it encourages\n"
            "- benefits: concrete advantages\n"
            "- drawbacks: tradeoffs or limitations\n"
            "- recommended_usage: short guidance on when and how to use it."
        )

    def recommendations_user(self, query: str, resource_data: str) -> str:
        return (
            f"Developer Query: {query}\n"
            f"Available Resources (JSON list): {resource_data}\n\n"
            "Based on the query and resources, provide a short recommendation (3-4 sentences) "
            f"for improving productivity. Mention:\n"
            "- which 1-2 resources to start with and why\n"
            "- main tradeoffs in terms of time/complexity\n"
            "- a next step the developer can take this week."
        )
