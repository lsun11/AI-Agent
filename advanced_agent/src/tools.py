from langchain.tools import tool
from .save_utils import save_result_document_raw

@tool
def save_results_tool(query: str, result_text: str) -> str:
    """
    Save the research results into a timestamped document in the 'saved_docs'
    folder. Use this when the user asks to save/export/log/record the results.
    """
    path = save_result_document_raw(query, result_text)
    return f"Results saved to: {path}"