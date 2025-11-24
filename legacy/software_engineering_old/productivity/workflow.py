from ..base_workflow import BaseSEWorkflow
from .models import (
    ProductivityResearchState,
    ProductivityCompanyInfo,
    ProductivityCompanyAnalysis,
)
from .prompts import ProductivityPrompts


class ProductivityWorkflow(
    BaseSEWorkflow[ProductivityResearchState, ProductivityCompanyInfo, ProductivityCompanyAnalysis]
):
    """Workflow specialized for the 'productivity' software engineering subtopic."""

    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        super().__init__(
            state_model=ProductivityResearchState,
            company_model=ProductivityCompanyInfo,
            analysis_model=ProductivityCompanyAnalysis,
            prompts=ProductivityPrompts(),
            model_name=model_name,
            temperature=temperature,
        )
