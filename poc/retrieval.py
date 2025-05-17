from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType, SearchableField  # import models from the correct submodule
from azure.core.credentials import AzureKeyCredential
from config import SEARCH_SERVICE_ENDPOINT, SEARCH_API_KEY

# Update Search Clients to use AzureKeyCredential
search_client = SearchClient(
    endpoint=SEARCH_SERVICE_ENDPOINT,
    index_name="documents-index",
    credential=AzureKeyCredential(SEARCH_API_KEY)
)

index_client = SearchIndexClient(
    endpoint=SEARCH_SERVICE_ENDPOINT,
    credential=AzureKeyCredential(SEARCH_API_KEY)
)

def create_index():
    """Creates an Azure AI Search index with the correct schema."""
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String, searchable=True, filterable=False, sortable=False)
    ]

    index = SearchIndex(name="documents-index", fields=fields)
    try:
        index_client.delete_index(index.name)
        print(" Deleted existing index")
    except Exception as e:
        print("No existing index to delete.")

    index_client.create_index(index)
    print(" Created Search Index with the correct schema")

def upload_documents():
    """Uploads sample documents for Azure Search."""
    documents = [
        {"id": "1", "content": "The nearest hydrogen producer in Mannheim is XYZ Energy."},
        {"id": "2", "content": "Hydrogen producers in Germany include XYZ Energy in Mannheim and ABC Hydrogen in Berlin."},
        {"id": "3", "content": "Hydrogen is a clean energy source produced by companies like XYZ Energy and ABC Hydrogen."},
        {"id": "4", "content": "For more details on hydrogen producers, visit our website or contact us directly."},
        {"id": "5", "content": "Hydrogen Solutions GmbH operates a large hydrogen production facility in Frankfurt am Main, producing green hydrogen via electrolysis."},
        {"id": "6", "content": "Frankfurt Hydrogen Center in Frankfurt produces over 10 tons of hydrogen per day, serving industrial clients in the Rhine-Main region."}
    ]

    search_client.upload_documents(documents)
    print("Uploaded Documents for Azure Search")

def get_retrieval_context(query: str) -> str:
    """Retrieves relevant context from Azure AI Search."""
    results = search_client.search(query)
    context_strings = [f"Document: {result['content']}" for result in results]
    return "\n\n".join(context_strings) if context_strings else "No results found."

def test_azure_search_connection():
    """Tests the connection to Azure Search and prints the document count."""
    try:
        search_client = SearchClient(
            endpoint=SEARCH_SERVICE_ENDPOINT,
            index_name="documents-index",
            credential=AzureKeyCredential(SEARCH_API_KEY)
        )
        document_count = search_client.get_document_count()
        print(f"Connection successful. Document count: {document_count}")
    except Exception as e:
        print(f" Failed to connect to Azure Search: {e}")

if __name__ == "__main__":
    test_azure_search_connection()
    query = "nearest hydrogen producer in Germany"
    print(f"Testing retrieval for query: '{query}'")
    context = get_retrieval_context(query)
    print(f"Retrieved Context:\n{context}")
