import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
import tools

load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)


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
    ),
    Tool(
        name="list_webapp_status",
        func=tools.list_webapp_status,
        description="Use this tool to list the specific status (running, exited, unhealthy) of all webapp containers (e.g., devopsagent-webapp-1, devopsagent-webapp-2). Useful for identifying which instances are actually down or stuck."
    )
]


prompt_template = """
You are an autonomous DevOps SRE agent. Your job is to diagnose and fix issues.

Follow these steps:
1. First, use 'check_webapp_health' on 'webapp' (the Nginx frontend) to see if the overall service is responsive. If it is healthy, your job is done.
2. If the webapp frontend is down, use 'list_webapp_status' to get the current state of all individual 'devopsagent-webapp-X' containers.
3. **Analyze the 'list_webapp_status' output.** For each 'devopsagent-webapp-X' container that has a status of 'exited' or 'unhealthy' (or is not in a 'running (Health: healthy)' state), consider it down.
4. **For each identified down or unhealthy 'devopsagent-webapp-X' container, use the 'restart_container' tool with its specific container name (e.g., 'devopsagent-webapp-1').** Restart them one by one.
5. After attempting to restart all identified down containers, use 'check_webapp_health' again to verify if the overall webapp frontend is back online. If it's still down, you might need to investigate logs using 'get_container_logs' for the recently restarted containers to find further clues, or list all running containers again.

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
Thought: I have taken all necessary actions and verified the state.
Final Answer: A final summary of what you did and the resolution.

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""


prompt = PromptTemplate.from_template(prompt_template)


agent = create_react_agent(llm=llm, tools=tool_list, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tool_list,
    verbose=True,
    handle_parsing_errors=True
)



if __name__ == "__main__":
    problem = sys.argv[1] if len(sys.argv) > 1 else "The webapp is down. Please investigate and resolve."
    print(f"--- Starting DevOps Agent for problem: {problem} ---")
    result = agent_executor.invoke({"input": problem})
    print("--- Agent Finished ---")
    print(result['output'])
