from ..base_prompts import BaseCSResearchPrompts


class DatabasePrompts(BaseCSResearchPrompts):
    """
    Prompts specialized for databases, data warehouses, and data platforms.
    """
    TOPIC_LABEL = "database, data warehouse, or data platform"
    ANALYSIS_SUBJECT = "databases, analytics platforms, and data infrastructure"
    RECOMMENDER_ROLE = "data infrastructure architect"
