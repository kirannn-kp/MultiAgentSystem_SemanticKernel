import os
from azure.core.credentials import AzureKeyCredential

# Azure AI Config
AZURE_MODEL_NAME = "gpt-4o-mini"
AZURE_ENDPOINT = os.getenv("AZURE_MODEL_ENDPOINT", "https://models.inference.ai.azure.com")
AZURE_CREDENTIAL = AzureKeyCredential(os.getenv("AZURE_OPENAI_KEY", "your_default_key"))

# Azure Search Config
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
INDEX_NAME = "custom-documents"  # Customizing index name
