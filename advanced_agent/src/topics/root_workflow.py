# src/topics/root_workflow.py
from __future__ import annotations

from typing import Optional, Callable, Any, List

from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_anthropic import ChatAnthropic

from ..firecrawl import FirecrawlService


class RootWorkflow:
    """
    Root workflow class shared by all specific topic/base workflows.

    Common responsibilities:
    - Hold the primary LLM instance (`self.llm`)
    - Manage log callbacks (`set_log_callback`, `_log`)
    - Switch models dynamically (`set_llm`)
    """

    # Subclasses are expected to define a topic_label if they want nicer logs.
    topic_label: str = "GenericTopic"
    topic_tag: str = "GenericSubTopic"
    def __init__(
        self,
        default_model: str = "gpt-4o-mini",
        default_temperature: float = 0.1,
    ) -> None:
        self.llm = ChatOpenAI(model=default_model, temperature=default_temperature)
        self._log_callback: Optional[Callable[[str], None]] = None
        self.firecrawl = FirecrawlService()

    # ---------------------------
    # LLM switching / configuration
    # ---------------------------
    def set_llm(self, model_name: str, temperature: float) -> None:
        """
        Dynamically change the underlying chat model.

        Subclasses still use `self.llm`, but how it's constructed is centralized here.
        """
        print(f"Setting LLM... model: {model_name} temperature: {temperature}")

        if "deepseek" in model_name:
            self.llm = ChatDeepSeek(model=model_name, temperature=temperature)
        elif "claude" in model_name:
            self.llm = ChatAnthropic(model=model_name, temperature=temperature)
        else:
            self.llm = ChatOpenAI(model=model_name, temperature=temperature)

    # ---------------------------
    # Logging
    # ---------------------------
    def set_log_callback(self, cb: Optional[Callable[[str], None]]) -> None:
        """
        Set a callback that will receive log lines (e.g. to stream to UI).
        """
        self._log_callback = cb

    def _log(self, msg: str) -> None:
        """
        Log a message with the topic label. Prints to console and, if set,
        forwards a simplified message to `_log_callback`.
        """
        text = f"[{self.topic_label} - {self.topic_tag}] {msg}"
        print(text)
        if self._log_callback:
            # If you prefer the full text, use `text` instead of `msg`
            self._log_callback(msg)


    # ------------------------------------------------------------------ #
    # Helper: normalize Firecrawl search results
    # ------------------------------------------------------------------ #
    def _get_web_results(self, search_results: Any) -> List[Any]:
        """Normalize Firecrawl search results into a list-like `web_results`."""
        if hasattr(search_results, "web"):
            return search_results.web  # SearchData.web
        if isinstance(search_results, dict):
            # Some docs/examples use dict-like shapes
            return search_results.get("web", []) or search_results.get("data", [])
        if isinstance(search_results, list):
            return search_results
        return []

    # ------------------------------------------------------------------ #
    # Helper: build article context from search results
    # ------------------------------------------------------------------ #
    def _build_all_content_from_results(self, web_results: List[Any]) -> str:
        all_content = ""

        for result in web_results:
            # result may be a Firecrawl Document or a dict
            markdown = getattr(result, "markdown", None)

            if markdown:
                all_content += markdown[:2000] + "\n\n"
                continue

            # Try fallback: scrape the URL if present
            url = None
            if hasattr(result, "metadata") and getattr(result, "metadata", None):
                url = getattr(result.metadata, "url", None)
            if not url:
                # Maybe result is dict-like
                if isinstance(result, dict):
                    url = result.get("url")

            if not url:
                continue

            scraped = self.firecrawl.scrape_company_pages(url)
            if scraped and getattr(scraped, "markdown", None):
                all_content += scraped.markdown[:2000] + "\n\n"

        return all_content