from autogen_ext.models.azure import AzureAIChatCompletionClient
from config import AZURE_MODEL_NAME, AZURE_ENDPOINT, AZURE_CREDENTIAL

# Initialize Azure AI Chat Completion Client
client = AzureAIChatCompletionClient(
    model=AZURE_MODEL_NAME,
    endpoint=AZURE_ENDPOINT,
    credential=AZURE_CREDENTIAL,
    model_info={
        "json_output": True,
        "function_calling": True,
        "vision": True,
        "family": "custom",
    },
)
