from langchain_core.messages import SystemMessage
from langchain.agents import create_agent
from agent.agent_simple import run_agent_simple
from agent.models import llm
from agent.prompts import system_prompt_with_context_tool
from agent.tools import retrieve_context, retrieve_search_results
import pandas as pd


# NOTE: This agent follows tool approch
tools = [retrieve_context, retrieve_search_results]

prompt = SystemMessage(system_prompt_with_context_tool)
agent = create_agent(llm, tools, system_prompt=prompt)


def run_agent_with_tool(user_input):
    obj = {"messages": [{"role": "user", "content": user_input}]}
    response = agent.invoke(obj)
    final_content = response["messages"][-1].content

    return final_content


def test_agent():
    file_path = "../docs/test_data2.csv"
    df = pd.read_csv(file_path)
    df["output_tool"] = df["query"].apply(run_agent_with_tool)
    df["output_simple"] = df["query"].apply(run_agent_simple)
    df.to_csv(file_path, index=False)


if __name__ == "__main__":
    test_agent()
