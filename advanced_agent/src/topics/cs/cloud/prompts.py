from ..base_prompts import BaseCSResearchPrompts


class CloudServicePrompts(BaseCSResearchPrompts):
    """
    Prompts specialized for API-based platforms, developer APIs, and integrations.
    """

    TOPIC_LABEL = "cloud service, infrastructure platform, or managed resource"
    ANALYSIS_SUBJECT = "cloud computing platforms, infrastructure services, and DevOps tools"
    RECOMMENDER_ROLE = "cloud infrastructure architect"
