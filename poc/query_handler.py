import time
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage
from azure_client import client
from search_index import search_client, documents
from evaluator import RAGEvaluator

# Create Assistant Agent
assistant = AssistantAgent(
    name="assistant",
    model_client=client,
    system_message="You are an AI assistant providing answers based on retrieved documents only."
)

def get_retrieval_context(query: str) -> str:
    results = search_client.search(query)
    context_strings = [f"Document: {result['content']}" for result in results]
    return "\n\n".join(context_strings) if context_strings else "No results found"

async def ask_rag(query: str, evaluator: RAGEvaluator):
    try:
        retrieval_context = get_retrieval_context(query)
        augmented_query = f"Retrieved Context:\n{retrieval_context}\n\nUser Query: {query}"

        start_time = time.time()
        response = await assistant.on_messages(
            [TextMessage(content=augmented_query, source="user")],
            cancellation_token=CancellationToken(),
        )
        processing_time = time.time() - start_time

        metrics = evaluator.evaluate_response(
            query=query,
            response=response.chat_message.content,
            context=documents
        )
        return {
            'response': response.chat_message.content,
            'processing_time': processing_time,
            'metrics': metrics,
        }
    except Exception as e:
        print(f"Error processing query: {e}")
        return None
