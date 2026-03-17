from langchain_core.messages import SystemMessage
from langchain.agents import create_agent
from agent.agent_simple import run_agent_simple
from agent.models import llm
from agent.prompts import system_prompt_with_context_tool
from agent.tools import retrieve_context, retrieve_search_results
import pandas as pd

from pydantic import BaseModel, Field


class LegalResponse(BaseModel):
    answer: str = Field(
        description="Answer to the user's query based on the retrieved context and search results. Strictly limit the response to under 200 words"
    )
    thread_title: str = Field(description="Title of the thread. Max 5 words.")


from langchain_core.output_parsers import PydanticOutputParser

output_parser = PydanticOutputParser(pydantic_object=LegalResponse)

# NOTE: This agent follows tool approch
tools = [retrieve_context, retrieve_search_results]

prompt = SystemMessage(system_prompt_with_context_tool)
message_agent = create_agent(llm, tools, system_prompt=prompt)
thread_agent = create_agent(
    llm,
    tools,
    system_prompt=SystemMessage(
        system_prompt_with_context_tool
        + "MUST return a JSON object with the following format: "
        + output_parser.get_format_instructions()
    ),
    response_format=LegalResponse,
)


def run_agent_with_tool(user_input: str) -> str:
    obj = {"messages": [{"role": "user", "content": user_input}]}
    response = message_agent.invoke(obj)
    final_content = response["messages"][-1].content

    return final_content.text if final_content else ""


async def run_agent_with_tool_memory(
    messages: list[dict],
    get_thread_title: bool = True,
) -> dict:
    obj = {"messages": messages}

    if get_thread_title:
        print("Invoking thread agent")
        response = await thread_agent.ainvoke(obj)

        final_content = response["messages"][-1].content
        print("Final content from thread agent:", final_content)
        try:
            final_content = output_parser.parse(final_content)
        except Exception as e:
            print("Error parsing output:", e)

        return {
            "response": final_content.answer if final_content else "",
            "thread_title": final_content.thread_title if final_content else "",
        }

    else:
        print("Invoking message agent")
        response = await message_agent.ainvoke(obj)
        final_content = response["messages"][-1].content

        return {"response": final_content if final_content else ""}


def test_agent():
    file_path = "../docs/test_data2.csv"
    df = pd.read_csv(file_path)
    df["output_tool"] = df["query"].apply(run_agent_with_tool)
    df["output_simple"] = df["query"].apply(run_agent_simple)
    df.to_csv(file_path, index=False)


if __name__ == "__main__":
    test_agent()
