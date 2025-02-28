from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType, SearchableField
from config import SEARCH_SERVICE_ENDPOINT, SEARCH_API_KEY

# Create Search Clients
search_client = SearchClient(
    endpoint=SEARCH_SERVICE_ENDPOINT,
    index_name="documents-index",
    credential=SEARCH_API_KEY
)

index_client = SearchIndexClient(
    endpoint=SEARCH_SERVICE_ENDPOINT,
    credential=SEARCH_API_KEY
)

def create_index():
    """Creates an Azure AI Search index."""
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String)
    ]
    
    index = SearchIndex(name="documents-index", fields=fields)
    index_client.create_index(index)
    print(" Created Search Index")

def upload_documents():
    """Uploads sample documents."""
    documents = [
        {"id": "1", "content": "Contoso Travel offers luxury vacations."},
        {"id": "2", "content": "Our travel insurance covers medical emergencies."}
    ]
    
    search_client.upload_documents(documents)
    print("Uploaded Documents")

def get_retrieval_context(query: str) -> str:
    """Retrieves relevant context from Azure AI Search."""
    results = search_client.search(query)
    context_strings = [f"Document: {result['content']}" for result in results]
    return "\n\n".join(context_strings) if context_strings else "No results found."
