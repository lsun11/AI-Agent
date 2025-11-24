from typing import Dict, Any, Callable, Optional, List, Type

from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from ...firecrawl import FirecrawlService
from .base_models import (
    BaseSoftwareEngState,
    BaseSoftwareEngResourceSummary,
    BaseSoftwareEngRecommendation,
)
from .base_prompts import BaseSoftwareEngPrompts
from ..root_workflow import RootWorkflow

LogCallback = Callable[[str], None]


class BaseSoftwareEngWorkflow(RootWorkflow):
    state_model: Type[BaseSoftwareEngState] = BaseSoftwareEngState
    resource_model: Type[BaseSoftwareEngResourceSummary] = BaseSoftwareEngResourceSummary
    recommendation_model: Type[BaseSoftwareEngRecommendation] = BaseSoftwareEngRecommendation
    prompts_cls: Type[BaseSoftwareEngPrompts] = BaseSoftwareEngPrompts
    topic_label: str = "Software Engineering"

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.1,
    ) -> None:
        # initialize RootWorkflow (sets self.llm and _log_callback)
        super().__init__(
            default_model=model,
            default_temperature=temperature,
        )
        self.prompts = self.prompts_cls()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(self.state_model)
        graph.add_node("extract_resources", self._extract_resources_step)
        graph.add_node("analyze", self._analyze_step)
        graph.add_node("recommend", self._recommend_step)
        graph.set_entry_point("extract_resources")
        graph.add_edge("extract_resources", "analyze")
        graph.add_edge("analyze", "recommend")
        graph.add_edge("recommend", END)
        return graph.compile()


    def _extract_resources_step(self, state: BaseSoftwareEngState) -> Dict[str, Any]:
        self._log(f"Finding articles/resources about: {state.query}")

        article_query = f"{state.query} best practices guide"
        search_results = self.firecrawl.search_companies(article_query, num_results=3)
        print("_extract_tools_step, check0")
        web_results = self._get_web_results(search_results)
        print("_extract_tools_step, check1")
        all_content = ""
        resources: list[BaseSoftwareEngResourceSummary] = []
        print("_extract_tools_step, check2")
        for doc in web_results:
            markdown = getattr(doc, "markdown", None)
            meta = getattr(doc, "metadata", None)
            title = getattr(meta, "title", "") if meta else ""
            url = getattr(meta, "url", "") if meta else ""

            if markdown:
                snippet = markdown[:1500]
                all_content += snippet + "\n\n"
            else:
                if url:
                    scraped = self.firecrawl.scrape_company_pages(url)
                    if scraped and getattr(scraped, "markdown", None):
                        snippet = scraped.markdown[:1500]
                        all_content += snippet + "\n\n"
                else:
                    continue

            if url or title:
                resources.append(
                    self.resource_model(
                        title=title or "Untitled resource",
                        url=url or "",
                        key_points=[],
                        concepts=[],
                        recommended_tools=[],
                    )
                )

        if not all_content:
            self._log("No content found; continuing with empty extraction.")
            return {"resources": resources, "extracted_keywords": []}

        messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(state.query, all_content)),
        ]

        try:
            response = self.llm.invoke(messages)
            lines = [
                ln.strip()
                for ln in response.content.split("\n")
                if ln.strip()
            ]
            self._log(f"Extracted keywords/concepts: {', '.join(lines[:10])}")
            return {
                "resources": resources,
                "extracted_keywords": lines,
            }
        except Exception as e:
            self._log(f"Extraction failed: {e}")
            return {"resources": resources, "extracted_keywords": []}

    def _analyze_step(self, state: BaseSoftwareEngState) -> Dict[str, Any]:
        self._log("Analyzing aggregated resources")

        combined = ""
        for res in state.resources[:3]:
            if not res.url:
                continue
            scraped = self.firecrawl.scrape_company_pages(res.url)
            if scraped and getattr(scraped, "markdown", None):
                combined += scraped.markdown[:2000] + "\n\n"

        if not combined:
            self._log("No detailed content to analyze; skipping analysis.")
            return {}
        structured_llm = self.llm.with_structured_output(self.recommendation_model)
        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(self.topic_label, combined)),
        ]
        try:
            analysis = structured_llm.invoke(messages)
            return {"analysis": analysis}
        except Exception as e:
            self._log(f"Analysis failed: {e}")
            fallback = self.recommendation_model(
                summary="Analysis failed.",
                best_practices=[],
                pitfalls=[],
                suggested_action_plan=[],
            )
            return {"analysis": fallback}

    def _recommend_step(self, state: BaseSoftwareEngState) -> Dict[str, Any]:
        self._log("Generating final recommendations")

        import json

        resources_json = json.dumps(
            [r.model_dump() for r in state.resources],
            ensure_ascii=False,
        )

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(
                content=self.prompts.recommendations_user(
                    state.query,
                    resources_json,
                )
            ),
        ]

        response = self.llm.invoke(messages)
        if state.analysis:
            state.analysis.summary = response.content
            return {"analysis": state.analysis}

        fallback = self.recommendation_model(
            summary=response.content,
            best_practices=[],
            pitfalls=[],
            suggested_action_plan=[],
        )
        return {"analysis": fallback}

    def run(self, query: str) -> BaseSoftwareEngState:
        initial_state = self.state_model(query=query)
        final_state = self.workflow.invoke(initial_state)
        return self.state_model(**final_state)
