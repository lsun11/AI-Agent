import os
import concurrent.futures
from typing import Any

from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

class FirecrawlService:
    def __init__(self, timeout_seconds: float = 60.0):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Environment variable FIRECRAWL_API_KEY not found")

        self.app = FirecrawlApp(api_key=api_key)

        # Caches to avoid unnecessary external calls
        self._search_cache: dict[tuple[str, int], Any] = {}
        self._scrape_cache: dict[str, Any] = {}

        self.timeout_seconds = timeout_seconds

    # ------------------------------------------------------------
    # 🔍 SEARCH with forced timeout
    # ------------------------------------------------------------
    def search_companies(self, query: str, num_results: int = 5):
        key = (query, num_results)
        if key in self._search_cache:
            return self._search_cache[key]

        print(f"Searching company pricing for: {query}")

        def _do_search():
            return self.app.search(
                query=f"{query} company pricing",
                limit=num_results,
                scrape_options={ "formats": ["markdown"] },
            )

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_do_search)
                result = future.result(timeout=self.timeout_seconds)

        except concurrent.futures.TimeoutError:
            print(f"[TIMEOUT] search took longer than {self.timeout_seconds}s for '{query}'")
            return []

        except Exception as e:
            print(f"[ERROR] search failed for '{query}': {e}")
            return []

        # Optional sanity check
        if not result:
            print(f"[WARN] search returned empty result for '{query}'")
            return []

        self._search_cache[key] = result
        return result

    # ------------------------------------------------------------
    # 🌐 SCRAPE with forced timeout
    # ------------------------------------------------------------
    def scrape_company_pages(self, url: str):
        if url in self._scrape_cache:
            return self._scrape_cache[url]

        print("Scraping", url)

        def _do_scrape():
            return self.app.scrape(
                url=url,
                formats=["markdown"],
            )

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_do_scrape)
                result = future.result(timeout=self.timeout_seconds)

        except concurrent.futures.TimeoutError:
            print(f"[TIMEOUT] scrape took longer than {self.timeout_seconds}s for {url}")
            return None

        except Exception as e:
            print(f"[ERROR] scrape failed for {url}: {e}")
            return None

        if not result:
            print(f"[WARN] scrape returned empty result for {url}")
            return None

        self._scrape_cache[url] = result
        return result



