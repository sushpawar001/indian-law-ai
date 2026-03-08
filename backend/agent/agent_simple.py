from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage
from db.db import vector_store

load_dotenv()

OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")

# NOTE: This agent follows simple approch
llm = ChatOpenAI(
    model="arcee-ai/trinity-large-preview:free",
    api_key=OPEN_ROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.3,
    max_completion_tokens=2000,
)


def run_agent_simple(user_input):
    results = vector_store.similarity_search(user_input, k=3)
    formatted_result = ""
    for doc in results:
        act_number = doc.metadata.get("Act Number")
        short_title = doc.metadata.get("Short Title")

        if act_number:
            formatted_result += f"Act Number: {act_number}"

        if short_title:
            formatted_result += f"Short Title: {short_title}"

        formatted_result += f"{doc.page_content}\n"

    print("Found articles", len(results))

    messages = [
        SystemMessage(
            f"You are an expert legal assistant specialized in making complex law accessible to the general public. Your goal is to answer the user's query using only the provided context. If the answer isn't in the context, honestly state that you don't have enough information. While answering mention Act number and title.\n{formatted_result}"
        ),
        HumanMessage(user_input),
    ]

    response = llm.invoke(messages)

    return response.content
