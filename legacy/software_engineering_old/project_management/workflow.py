from ..base_workflow import BaseSEWorkflow
from .models import (
    ProjectManagementResearchState,
    ProjectManagementCompanyInfo,
    ProjectManagementCompanyAnalysis,
)
from .prompts import ProjectManagementPrompts


class ProjectManagementWorkflow(
    BaseSEWorkflow[ProjectManagementResearchState, ProjectManagementCompanyInfo, ProjectManagementCompanyAnalysis]
):
    """Workflow specialized for the 'project management' software engineering subtopic."""

    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        super().__init__(
            state_model=ProjectManagementResearchState,
            company_model=ProjectManagementCompanyInfo,
            analysis_model=ProjectManagementCompanyAnalysis,
            prompts=ProjectManagementPrompts(),
            model_name=model_name,
            temperature=temperature,
        )
