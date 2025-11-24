from ..base_workflow import BaseSEWorkflow
from .models import (
    CodeReviewResearchState,
    CodeReviewCompanyInfo,
    CodeReviewCompanyAnalysis,
)
from .prompts import CodeReviewPrompts


class CodeReviewWorkflow(
    BaseSEWorkflow[CodeReviewResearchState, CodeReviewCompanyInfo, CodeReviewCompanyAnalysis]
):
    """Workflow specialized for the 'code review' software engineering subtopic."""

    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        super().__init__(
            state_model=CodeReviewResearchState,
            company_model=CodeReviewCompanyInfo,
            analysis_model=CodeReviewCompanyAnalysis,
            prompts=CodeReviewPrompts(),
            model_name=model_name,
            temperature=temperature,
        )
