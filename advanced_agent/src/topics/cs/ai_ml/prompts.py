from ..base_prompts import BaseCSResearchPrompts


class AIPlatformPrompts(BaseCSResearchPrompts):
    """
    Prompts specialized for AI/ML platforms (LLMs, model hosting, vector DB, training services).
    """
    TOPIC_LABEL = "AI/ML platform, model API, or machine-learning service"
    ANALYSIS_SUBJECT = "AI platforms, model hosting solutions, vector DBs, and ML tooling"
    RECOMMENDER_ROLE = "machine learning systems engineer"
