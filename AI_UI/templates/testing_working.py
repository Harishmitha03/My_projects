import httpx
from langchain_community.chat_models import ChatOpenAI

base_url = "https://genailab.tcs.in"
api_key = "sk-oU4skvhrOX0f6oyZ3cHLQA"

# Create an HTTP client that ignores SSL certificate verification
client = httpx.Client(verify=False)

# Initialize the LLM
llm = ChatOpenAI(
    base_url=base_url,
    model="genailab-maas-gpt-35-turbo",
    api_key=api_key,
    http_client=client
)

# Test the call
response = llm.invoke("what is gen ai")
print(response.content)