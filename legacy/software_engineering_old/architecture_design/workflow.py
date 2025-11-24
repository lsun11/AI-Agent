from ..base_workflow import BaseSEWorkflow
from .models import (
    ArchitectureDesignResearchState,
    ArchitectureDesignCompanyInfo,
    ArchitectureDesignCompanyAnalysis,
)
from .prompts import ArchitectureDesignPrompts


class ArchitectureDesignWorkflow(
    BaseSEWorkflow[ArchitectureDesignResearchState, ArchitectureDesignCompanyInfo, ArchitectureDesignCompanyAnalysis]
):
    """Workflow specialized for the 'architecture design' software engineering subtopic."""

    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        super().__init__(
            state_model=ArchitectureDesignResearchState,
            company_model=ArchitectureDesignCompanyInfo,
            analysis_model=ArchitectureDesignCompanyAnalysis,
            prompts=ArchitectureDesignPrompts(),
            model_name=model_name,
            temperature=temperature,
        )
