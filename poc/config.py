import os
from azure.identity import DefaultAzureCredential

# Azure AI Foundry Connection String (Set in your environment)
PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")

# Azure AI Search Credentials
SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

# Azure Credentials
AZURE_CREDENTIAL = DefaultAzureCredential()
