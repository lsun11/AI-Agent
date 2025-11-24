from typing import Dict, Any, Type, TypeVar, Generic, Callable, Optional, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from advanced_agent.src.firecrawl import FirecrawlService
from .base_models import BaseSEResearchState, BaseSECompanyInfo, BaseSECompanyAnalysis
from .base_prompts import BaseSEPrompts


StateT = TypeVar("StateT", bound=BaseSEResearchState)
CompanyT = TypeVar("CompanyT", bound=BaseSECompanyInfo)
AnalysisT = TypeVar("AnalysisT", bound=BaseSECompanyAnalysis)


class BaseSEWorkflow(Generic[StateT, CompanyT, AnalysisT]):
    """Generic workflow for software engineering research topics.

    Subtopics should subclass and supply concrete State/Company/Analysis models
    plus a specialized prompt class instance.
    """
    topic_label: str = "Software Eng"
    def __init__(
        self,
        state_model: Type[StateT],
        company_model: Type[CompanyT],
        analysis_model: Type[AnalysisT],
        prompts: BaseSEPrompts,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.1,
    ):
        self.state_model = state_model
        self.company_model = company_model
        self.analysis_model = analysis_model
        self.prompts = prompts

        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self._log_callback: Optional[Callable[[str], None]] = None
        self.workflow = self._build_workflow()

    # --------- plumbing ----------
    def set_llm(self, model_name: str, temperature: float) -> None:
        print("Setting LLM... model:", model_name, "temperature:", temperature)
        if "deepseek" in model_name:
            self.llm = ChatDeepSeek(model=model_name, temperature=temperature)
        elif "claude" in model_name:
            self.llm = ChatAnthropic(model=model_name, temperature=temperature)
        else:
            self.llm = ChatOpenAI(model=model_name, temperature=temperature)

    def set_log_callback(self, cb: Optional[Callable[[str], None]]) -> None:
        self._log_callback = cb

    def _log(self, msg: str) -> None:
        text = f"[{self.topic_label}] {msg}"
        print(text)  # keep terminal behavior
        if self._log_callback:
            self._log_callback(msg)

    def _build_workflow(self):
        graph = StateGraph(self.state_model)
        graph.add_node("extract_resources", self._extract_resources_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)

        graph.set_entry_point("extract_resources")
        graph.add_edge("extract_resources", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)

        return graph.compile()

    # --------- Firecrawl helpers ----------

    def _get_web_results(self, search_results: Any) -> list:
        """Normalize Firecrawl search results into a list of web docs."""
        if hasattr(search_results, "web") and isinstance(search_results.web, list):
            return search_results.web
        if isinstance(search_results, dict):
            return search_results.get("web", [])
        if isinstance(search_results, list):
            return search_results
        return []

    # --------- core steps ----------

    def _extract_resources_step(self, state: StateT) -> Dict[str, Any]:
        self._log(f"Finding articles/resources about: {state.query}")

        article_query = f"{state.query} best practices tools frameworks"
        search_results = self.firecrawl.search_companies(article_query, num_results=3)
        web_results = self._get_web_results(search_results)

        all_content = ""
        for result in web_results:
            markdown = getattr(result, "markdown", None)
            if markdown:
                all_content += markdown
            else:
                url = getattr(result, "url", None) or (
                    result.get("url") if isinstance(result, dict) else ""
                )
                if not url:
                    continue
                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped and getattr(scraped, "markdown", None):
                    all_content += scraped.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(state.query, all_content)),
        ]

        try:
            response = self.llm.invoke(messages)
            names = [
                line.strip()
                for line in response.content.strip().split("\n")
                if line.strip()
            ]
            self._log(f"Extracted resources: {', '.join(names[:5])}")
            return {"extracted_resources": names}
        except Exception as e:
            self._log(f"Extraction error: {e}")
            return {"extracted_resources": []}

    def _analyze_single_resource(self, name: str, content: str) -> AnalysisT:
        structured_llm = self.llm.with_structured_output(self.analysis_model)
        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(name, content)),
        ]
        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            self._log(f"Analysis error for {name}: {e}")
            return self.analysis_model(
                primary_focus="Unknown",
                difficulty_level=None,
                ideal_audience=[],
                key_practices=[],
                benefits=[],
                drawbacks=[],
                recommended_usage="Analysis failed.",
            )

    def _research_step(self, state: StateT) -> Dict[str, Any]:
        names = getattr(state, "extracted_resources", []) or []

        if not names:
            self._log("No extracted resources found, falling back to direct search")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            web_results = self._get_web_results(search_results)
            names = []
            for doc in web_results[:4]:
                title = getattr(getattr(doc, "metadata", None), "title", None)
                if not title and isinstance(doc, dict):
                    meta = doc.get("metadata") or {}
                    title = meta.get("title")
                if title:
                    names.append(title)

        names = names[:4]
        self._log(f"Researching specific resources: {', '.join(names)}")

        resources: List[CompanyT] = []

        for name in names:
            self._log(f"researching: {name}")
            tool_query = f"{name} official site"
            tool_search_results = self.firecrawl.search_companies(tool_query, num_results=1)
            web_results = self._get_web_results(tool_search_results)
            if not web_results:
                continue

            doc = web_results[0]
            meta = getattr(doc, "metadata", None)
            url = ""
            desc = ""
            if meta:
                url = getattr(meta, "url", "") or ""
                desc = getattr(meta, "description", "") or ""

            if not url:
                continue

            company: CompanyT = self.company_model(
                name=name,
                description=desc,
                website=url,
                category=None,
                tags=[],
                tech_stack=[],
                competitors=[],
            )
            print("Pre checking", company.name)
            scraped = self.firecrawl.scrape_company_pages(url)
            if scraped and getattr(scraped, "markdown", None):
                content = scraped.markdown
                analysis = self._analyze_single_resource(company.name, content)

                company.pricing_model = getattr(analysis, "pricing_model", None)
                company.pricing_details = getattr(analysis, "pricing_details", None)
                company.is_open_source = getattr(analysis, "is_open_source", None)
                company.tech_stack = getattr(analysis, "tech_stack", [])
                company.description = analysis.recommended_usage or company.description
            print("Finished:", company.name)
            resources.append(company)

        return {"resources": resources}

    def _analyze_step(self, state: StateT) -> Dict[str, Any]:
        self._log("Generating recommendations")

        resource_data = ", ".join([r.model_dump_json() for r in state.resources])
        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, resource_data)),
        ]

        response = self.llm.invoke(messages)
        return {"analysis": response.content}

    def run(self, query: str) -> StateT:
        initial_state = self.state_model(query=query)
        final_state = self.workflow.invoke(initial_state)
        return self.state_model(**final_state)
