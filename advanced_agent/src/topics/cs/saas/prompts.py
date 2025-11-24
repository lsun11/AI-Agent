from ..base_prompts import BaseCSResearchPrompts


class SaaSPrompts(BaseCSResearchPrompts):
    """
    Prompts specialized for researching SaaS products.
    """
    TOPIC_LABEL = "SaaS product, cloud application, or hosted service"
    ANALYSIS_SUBJECT = "SaaS platforms and hosted software products"
    RECOMMENDER_ROLE = "senior SaaS solutions architect"
