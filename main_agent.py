import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
import tools

load_dotenv()

# 1. Setup the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)

# 2. Define the Tools
tool_list = [
    Tool(
        name="list_running_containers",
        func=tools.list_running_containers,
        description="Use this tool to list all currently running docker containers."
    ),
    Tool(
        name="check_webapp_health",
        func=tools.check_webapp_health,
        description="Use this tool to check the health status of the main webapp service."
    ),
    Tool(
        name="restart_container",
        func=tools.restart_container,
        description="Use this tool to restart a specific container. You must provide the container's name or ID as an argument."
    ),
    Tool(
        name="get_container_logs",
        func=tools.get_container_logs,
        description="Use this to get the last 20 log lines from a specific container. You must provide the container's name or ID."
    )
]

# 3. Prompt Template (note: added {tool_names})
prompt_template = """
You are an autonomous DevOps SRE agent. Your job is to diagnose and fix issues.
Your primary webapp service is named 'webapp-service'.

Follow these steps:
1. First, use 'check_webapp_health'. If it is healthy, your job is done.
2. If the webapp is down, use 'list_running_containers' to see what is currently running.
3. Compare the list of running containers to the expected 'webapp-service'. The container that is missing is the one you need to restart.
4. Use the 'restart_container' tool on the 'webapp-service' container to fix the problem.

You have access to the following tools:
{tools}

When deciding which tool to use, you must use one of the following tool names:
{tool_names}

Use the following format for your thought process:

Question: the initial problem or observation you need to address
Thought: you should always think about what to do based on the previous observation.
Action: the action to take, should be one of the available tools from the list above
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: a final summary of what you did and the resolution.

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

# ✅ Do NOT use .partial() — LangChain fills {tools} and {tool_names} automatically
prompt = PromptTemplate.from_template(prompt_template)

# 4. Create the Agent
agent = create_react_agent(llm=llm, tools=tool_list, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tool_list,
    verbose=True,
    handle_parsing_errors=True
)


# 5. Run the Agent
if __name__ == "__main__":
    problem = sys.argv[1] if len(sys.argv) > 1 else "The webapp is down. Please investigate and resolve."
    print(f"--- Starting DevOps Agent for problem: {problem} ---")
    result = agent_executor.invoke({"input": problem})
    print("--- Agent Finished ---")
    print(result['output'])
