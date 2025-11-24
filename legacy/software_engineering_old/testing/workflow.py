from ..base_workflow import BaseSEWorkflow
from .models import (
    TestingResearchState,
    TestingCompanyInfo,
    TestingCompanyAnalysis,
)
from .prompts import TestingPrompts


class TestingWorkflow(
    BaseSEWorkflow[TestingResearchState, TestingCompanyInfo, TestingCompanyAnalysis]
):
    """Workflow specialized for the 'testing' software engineering subtopic."""

    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        super().__init__(
            state_model=TestingResearchState,
            company_model=TestingCompanyInfo,
            analysis_model=TestingCompanyAnalysis,
            prompts=TestingPrompts(),
            model_name=model_name,
            temperature=temperature,
        )
