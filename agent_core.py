import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from dotenv import load_dotenv


load_dotenv()


if os.getenv("GOOGLE_API_KEY") is None:
    print("Error: GOOGLE_API_KEY not found. Please set it in the .env file.")
    exit()


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)


prompt = PromptTemplate.from_template(
    """
    You are an expert DevOps agent. You are given a problem statement.
    Your goal is to create a step-by-step plan to resolve it.
    You cannot execute anything yet. Just provide the plan.

    Problem: {input}

    Plan:
    """
)


chain = prompt | llm


if __name__ == "__main__":
    problem_statement = "The service 'user-database' is not responding."

    print(f"--- Feeding problem to agent ---\n{problem_statement}\n")

    
    response = chain.invoke({"input": problem_statement})

    print("--- Agent's Proposed Plan ---")
    print(response.content)