import os
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

required_env_vars = [
    "AZURE_SEARCH_ENDPOINT", 
    "AZURE_SEARCH_API_KEY",
    "AZURE_SUBSCRIPTION_ID",
    "AZURE_RESOURCE_GROUP_NAME",
    "AZURE_PROJECT_NAME",
    "AZURE_AGENT_ID",
    "SPEECH_KEY",
    "SPEECH_REGION"
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Azure AI Search Credentials
SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")  
SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

AZURE_CREDENTIAL = AzureCliCredential()

SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
RESOURCE_GROUP_NAME = os.getenv("AZURE_RESOURCE_GROUP_NAME")
PROJECT_NAME = os.getenv("AZURE_PROJECT_NAME")
ASSISTANT_ID = os.getenv("AZURE_AGENT_ID") 

print(f"Debug: ASSISTANT_ID loaded as: {ASSISTANT_ID}")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
AZURE_OPENAI_RT_ENDPOINT = f"{OPENAI_ENDPOINT}/openai/realtime?api-version=2024-10-01-preview&deployment=gpt-4o-realtime-preview"
AZURE_OPENAI_RT_KEY = OPENAI_API_KEY