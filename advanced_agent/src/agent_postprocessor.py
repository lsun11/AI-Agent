from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from .tools import save_results_tool


def create_postprocess_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """
             You are a research assistant with access to tools.
             The user query + research results will be provided to you.
             If the user asked to save/export/store the results,
             then call the `save_results_tool`.
 
             If not, simply acknowledge completion.
         """
         ),
        ("human",
         """
         USER QUERY:
         {query}
 
         RESEARCH RESULTS:
         {result_text}
 
         Decide whether to save the results.
         """),
        ("placeholder", "{agent_scratchpad}")
    ])

    tools = [save_results_tool]

    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )

    return AgentExecutor(agent=agent, tools=tools, verbose=True)
