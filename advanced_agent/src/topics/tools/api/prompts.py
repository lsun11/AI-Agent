from ..base_prompts import BaseCSResearchPrompts


class APIPlatformPrompts(BaseCSResearchPrompts):
    """
    Prompts specialized for API-based platforms, developer APIs, and integrations.
    """

    TOPIC_LABEL = "API platform, developer API, or programmatic service"
    ANALYSIS_SUBJECT = "API platforms, REST/GraphQL services, and developer integrations"
    RECOMMENDER_ROLE = "API integration specialist"
