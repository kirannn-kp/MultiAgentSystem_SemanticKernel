import asyncio
from search_index import setup_index, upload_documents
from evaluator import RAGEvaluator
from query_handler import ask_rag

async def main():
    # Setup Index and Upload Documents
    setup_index()
    upload_documents()

    evaluator = RAGEvaluator()
    queries = [
        "Tell me about AI chatbots.",
        "How does cloud computing help businesses?"
    ]

    for query in queries:
        print(f"\nProcessing Query: {query}")
        result = await ask_rag(query, evaluator)
        if result:
            print("Response:", result['response'])
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
