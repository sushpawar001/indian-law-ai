from db.db import vector_store
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()


@tool("legal_doc_retrieval", response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    print(f"\nAgent is finding data for {query}\n")
    retrieved_docs = vector_store.similarity_search(query, k=3)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


@tool("similar_cases_retrieval")
def retrieve_search_results(web_search_query: str):
    """Retrieve search results supporting the act we found."""
    print(f"\nAgent is searching data for {web_search_query}\n")
    result = search_tool.run(web_search_query)

    return result
