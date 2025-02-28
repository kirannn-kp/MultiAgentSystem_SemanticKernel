from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType, SearchableField
from config import AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_API_KEY, INDEX_NAME
from azure.core.credentials import AzureKeyCredential

# Initialize Search Clients
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
)

index_client = SearchIndexClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
)

# Define Index Schema
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="content", type=SearchFieldDataType.String)
]

# Create Index if not exists
def setup_index():
    index = SearchIndex(name=INDEX_NAME, fields=fields)
    try:
        index_client.create_index(index)
        print(f"Index '{INDEX_NAME}' created successfully.")
    except Exception as e:
        print(f"Index setup error: {e}")

# Sample Documents (Updated Content)
documents = [
    {"id": "1", "content": "TechWorld provides latest updates on AI and machine learning."},
    {"id": "2", "content": "Our AI-powered chatbot helps automate customer interactions effectively."},
    {"id": "3", "content": "Cloud computing offers scalable infrastructure for enterprise applications."},
]

def upload_documents():
    try:
        search_client.upload_documents(documents)
        print("Documents uploaded successfully.")
    except Exception as e:
        print(f"Error uploading documents: {e}")
