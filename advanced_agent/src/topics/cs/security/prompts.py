from ..base_prompts import BaseCSResearchPrompts


class SecurityPrompts(BaseCSResearchPrompts):
    """
    Prompts specialized for cybersecurity platforms and authentication tools.

    It inherits the generic structure from BaseCSResearchPrompts but tunes the wording
    via these class-level attributes.

    NOTE: All attribute and method names are kept the same as your original class:
      - TOOL_EXTRACTION_SYSTEM
      - tool_extraction_user
      - TOOL_ANALYSIS_SYSTEM
      - tool_analysis_user
      - RECOMMENDATIONS_SYSTEM
      - recommendations_user

    So you can keep using `self.prompts.TOOL_EXTRACTION_SYSTEM`, etc.,
    without changing any of the rest of your code.
    """

    TOPIC_LABEL = "security tool, authentication service, or identity platform"
    ANALYSIS_SUBJECT = "cybersecurity tools, identity management systems, and authentication providers"
    RECOMMENDER_ROLE = "security engineer"
