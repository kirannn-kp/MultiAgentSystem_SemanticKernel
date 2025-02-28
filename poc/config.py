import os
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure AI Foundry Connection String (Set in your environment)
PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")

# Azure AI Search Credentials
SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")


AZURE_CREDENTIAL = SEARCH_API_KEY

# Additional required parameters
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
RESOURCE_GROUP_NAME = os.getenv("AZURE_RESOURCE_GROUP_NAME")
PROJECT_NAME = os.getenv("AZURE_PROJECT_NAME")
ASSISTANT_ID = os.getenv("AZURE_AGENT_ID")  # Add this line