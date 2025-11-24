from ..base_workflow import BaseSEWorkflow
from .models import (
    CodeQualityResearchState,
    CodeQualityCompanyInfo,
    CodeQualityCompanyAnalysis,
)
from .prompts import CodeQualityPrompts


class CodeQualityWorkflow(
    BaseSEWorkflow[CodeQualityResearchState, CodeQualityCompanyInfo, CodeQualityCompanyAnalysis]
):
    """Workflow specialized for the 'code quality' software engineering subtopic."""

    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        super().__init__(
            state_model=CodeQualityResearchState,
            company_model=CodeQualityCompanyInfo,
            analysis_model=CodeQualityCompanyAnalysis,
            prompts=CodeQualityPrompts(),
            model_name=model_name,
            temperature=temperature,
        )
