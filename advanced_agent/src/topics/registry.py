# src/topics/registry.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Any

# # Import your topic-specific workflows

# NOW REPLACED BY TOOLS LIBRARY!!!
# from .cs.developer_tools.workflow import DeveloperToolsWorkflow
# from .cs.saas.workflow import SaaSWorkflow
# from .cs.api.workflow import APIWorkflow
# from .cs.ai_ml.workflow import AIWorkflow
# from .cs.security.workflow import SecurityWorkflow
# from .cs.cloud.workflow import CloudWorkflow
# from .cs.database.workflow import DatabaseWorkflow


from .tools.developer_tools.workflow import DeveloperToolsWorkflow
from .tools.saas.workflow import SaaSWorkflow
from .tools.api.workflow import APIWorkflow
from .tools.ai_ml.workflow import AIWorkflow
from .tools.security.workflow import SecurityWorkflow
from .tools.cloud.workflow import CloudWorkflow
from .tools.database.workflow import DatabaseWorkflow


from .career.resume_tools.workflow import ResumeToolsWorkflow
from .career.job_search.workflow import JobSearchWorkflow
from .career.learning_platforms.workflow import LearningPlatformsWorkflow
from .career.coding_interview.workflow import CodingInterviewPlatformsWorkflow
from .career.system_design.workflow import SystemDesignPlatformsWorkflow
from .career.behavioral_interview.workflow import BehavioralInterviewToolsWorkflow
from .software_engineering.agile import AgileWorkflow
from .software_engineering.architecture_design.workflow import ArchitectureDesignWorkflow
from .software_engineering.cicd import CICDWorkflow
from .software_engineering.code_quality.workflow import CodeQualityWorkflow
# from .software_engineering.code_review.workflow import CodeReviewWorkflow
# from .software_engineering.productivity.workflow import ProductivityWorkflow
# from .software_engineering.project_management.workflow import ProjectManagementWorkflow
from .software_engineering.testing.workflow import TestingWorkflow



@dataclass
class TopicConfig:
    """
    Generic description of a research topic.

    key: internal key used in requests and routing.
    label: human-friendly label (for UI, logs, etc.).
    description: short text to explain what this topic covers.
    workflow_factory: function/class that returns a workflow instance.
    domain: optional logical domain (e.g. 'cs', 'finance', 'bio', etc.)
    """
    key: str
    label: str
    description: str
    workflow_factory: Callable[[], Any]
    domain: str = "cs"


TOPIC_CONFIGS: Dict[str, TopicConfig] = {
    "developer_tools": TopicConfig(
        key="developer_tools",
        label="Developer Tools",
        description="IDEs, editors, debuggers, build tools, CI/CD, and developer productivity tooling.",
        workflow_factory=DeveloperToolsWorkflow,
        domain="tools", # domain="cs",
    ),
    "saas": TopicConfig(
        key="saas",
        label="SaaS Products",
        description="Hosted subscription software (B2B/B2C SaaS apps, CRM, helpdesk, collaboration tools, etc.).",
        workflow_factory=SaaSWorkflow,
        domain="tools", # domain="cs",
    ),
    "api": TopicConfig(
        key="api",
        label="API Platforms",
        description="Platforms whose main product is an API/SDK: REST/GraphQL APIs, webhooks, API gateways, etc.",
        workflow_factory=APIWorkflow,
        domain="tools", # domain="cs",
    ),
    "ai_ml": TopicConfig(
        key="ai_ml",
        label="AI & ML Platforms",
        description="LLM providers, ML platforms, model hosting, vector DBs, embeddings, fine-tuning, AI infra.",
        workflow_factory=AIWorkflow,
        domain="tools", # domain="cs",
    ),
    "security": TopicConfig(
        key="security",
        label="Security & Identity",
        description="Auth, identity, IAM, SSO, OAuth/OIDC, MFA, zero trust, WAF, bot/fraud detection, security tools.",
        workflow_factory=SecurityWorkflow,
        domain="tools", # domain="cs",
    ),
    "cloud": TopicConfig(
        key="cloud",
        label="Cloud & Infrastructure",
        description="Cloud providers and infra: compute, storage, networking, serverless, managed Kubernetes, etc.",
        workflow_factory=CloudWorkflow,
        domain="tools", # domain="cs",
    ),
    "database": TopicConfig(
        key="database",
        label="Databases & Data Platforms",
        description="SQL/NoSQL DBs, data warehouses, OLTP/OLAP engines, and managed database services.",
        workflow_factory=DatabaseWorkflow,
        domain="tools", # domain="cs",
    ),

    # ==== Career domain ====
    "resume_tools": TopicConfig(
        key="resume_tools",
        label="Resume Optimization & ATS Tools",
        description="Resume builders, ATS checkers, keyword optimizers and related tools.",
        workflow_factory=ResumeToolsWorkflow,
        domain="career",
    ),
    "job_search": TopicConfig(
        key="job_search",
        label="Job Search Platforms & Market Analysis",
        description="Job boards, remote job sites, and salary/market insight platforms.",
        workflow_factory=JobSearchWorkflow,
        domain="career",
    ),
    "learning_platform": TopicConfig(
        key="learning_platform",
        label="Learning Platforms & Skill Roadmaps",
        description="Online courses, bootcamps, and structured learning roadmaps.",
        workflow_factory=LearningPlatformsWorkflow,
        domain="career",
    ),
    "coding_interview": TopicConfig(
        key="coding_interview",
        label="Coding Interview Platforms",
        description="Platforms for coding interview practice and mock interviews.",
        workflow_factory=CodingInterviewPlatformsWorkflow,
        domain="career",
    ),
    "system_design": TopicConfig(
        key="system_design",
        label="System Design Interview Platforms",
        description="System design interview preparation platforms and resources.",
        workflow_factory=SystemDesignPlatformsWorkflow,
        domain="career",
    ),
    "behavioral_interview": TopicConfig(
        key="behavioral_interview",
        label="Behavioral Interview & Coaching Tools",
        description="Behavioral interview practice tools and career coaching platforms.",
        workflow_factory=BehavioralInterviewToolsWorkflow,
        domain="career",
    ),
    # ==== Software engineering domain ====
    "architecture_design": TopicConfig(
        key="architecture_design",
        label="Architecture Design Suggestions",
        description="Suggestions for architecture design.",
        workflow_factory=ArchitectureDesignWorkflow,
        domain="software_engineering",
    ),
    "code_quality": TopicConfig(
        key="code_quality",
        label="Code Quality Suggestions",
        description="Suggestions for code quality.",
        workflow_factory=CodeQualityWorkflow,
        domain="software_engineering",
    ),
    # "code_review": TopicConfig(
    #     key="code_review",
    #     label="Code Review Suggestions",
    #     description="Suggestions for code review.",
    #     workflow_factory=CodeReviewWorkflow,
    #     domain="software_engineering_old",
    # ),
    # "productivity": TopicConfig(
    #     key="productivity",
    #     label="Productivity Suggestions",
    #     description="Suggestions for software engineering productivity.",
    #     workflow_factory=ProductivityWorkflow,
    #     domain="software_engineering_old",
    # ),
    # "project_management": TopicConfig(
    #     key="project_management",
    #     label="Project Management",
    #     description="Project management tools & suggestions for project management.",
    #     workflow_factory=ProjectManagementWorkflow,
    #     domain="software_engineering_old",
    # ),
    "testing": TopicConfig(
        key="testing",
        label="Testing",
        description="Testing tools & suggestions for testing.",
        workflow_factory=TestingWorkflow,
        domain="software_engineering",
    ),
    "agile": TopicConfig(
        key="agile",
        label="Agile Tools",
        description="Agile tools & suggestions.",
        workflow_factory=AgileWorkflow,
        domain="software_engineering",
    ),
    "cicd": TopicConfig(
        key="cicd",
        label="CICD Tools",
        description="CICD tools & suggestions.",
        workflow_factory=CICDWorkflow,
        domain="software_engineering",
    )
}


def build_workflows() -> Dict[str, Any]:
    """
    Instantiate one workflow per topic key.
    If you want lazy creation later, you can change this to return a factory.
    """
    return {key: cfg.workflow_factory() for key, cfg in TOPIC_CONFIGS.items()}

def get_topic_labels() -> Dict[str, str]:
    """
    Returns: { topic_key: label }
    """
    return {key: cfg.label for key, cfg in TOPIC_CONFIGS.items()}

def get_topic_descriptions() -> Dict[str, str]:
    """
    Returns: { topic_key: description }
    Used by the LLM router; no server hard-coding needed.
    """
    return {key: cfg.description for key, cfg in TOPIC_CONFIGS.items()}
