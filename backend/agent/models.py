from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatOpenAI(
    model="stepfun/step-3.5-flash:free",
    api_key=OPEN_ROUTER_KEY,  # type: ignore
    base_url="https://openrouter.ai/api/v1",
    temperature=0.2,
    max_completion_tokens=2000,
)

# llm = ChatGoogleGenerativeAI(
#     api_key=GEMINI_API_KEY,
#     model="gemini-2.5-flash",
#     temperature=0,  # Gemini 3.0+ defaults to 1.0
#     max_tokens=3000,
#     timeout=None,
#     max_retries=0,
# )
