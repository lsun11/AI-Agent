# src/topics/developer_tools/base_prompts.py
from __future__ import annotations

from ..base_prompts import BaseCSResearchPrompts


class DeveloperToolsPrompts(BaseCSResearchPrompts):
    """
    Prompt set specialized for *developer tools*.
    """

    # Customize the generic labels for this specific topic
    TOPIC_LABEL = "developer tool, library, platform, or service"
    ANALYSIS_SUBJECT = "developer tools and programming technologies"
    RECOMMENDER_ROLE = "senior software engineer"
