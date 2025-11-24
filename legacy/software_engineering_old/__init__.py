"""Software Engineering domain package.

Contains base models, prompts, and workflows for software engineering practice,
plus specialized subtopics like code quality, architecture, testing, etc.
"""

from .base_models import (
    BaseSECompanyAnalysis,
    BaseSECompanyInfo,
    BaseSEResearchState,
)

from .base_prompts import BaseSEPrompts
from .base_workflow import BaseSEWorkflow
