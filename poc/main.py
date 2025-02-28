import asyncio
from pathlib import Path
from azure.ai.projects.models import TextMessage
from azure.ai.projects import AIProjectClient
from config import PROJECT_CONNECTION_STRING, AZURE_CREDENTIAL
from agent import create_ai_agent
from retrieval import get_retrieval_context, upload_documents
from evaluator import RAGEvaluator

async def ask_rag(query: str, project_client: AIProjectClient, agent, evaluator: RAGEvaluator):
    """Processes query using RAG and evaluates the response."""
    try:
        retrieval_context = get_retrieval_context(query)

        augmented_query = (
            f"Retrieved Context:\n{retrieval_context}\n\n"
            f"User Query: {query}\n\n"
            "Based ONLY on the above context, please provide the answer."
        )

        thread = project_client.agents.create_thread()
        message = project_client.agents.create_message(thread_id=thread.id, role="user", content=augmented_query)
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)

        # Wait for AI to complete processing
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")
            return None

        messages = project_client.agents.list_messages(thread_id=thread.id)
        last_msg = messages.get_last_text_message_by_role("assistant")

        if last_msg:
            response_text = last_msg.text.value
            metrics = evaluator.evaluate_response(query, response_text, [])
            return {"response": response_text, "metrics": metrics}
        return None
    except Exception as e:
        print(f"Error processing query: {e}")
        return None

async def main():
    """Runs the full RAG pipeline."""
    project_client, agent = create_ai_agent()
    evaluator = RAGEvaluator()
    
    queries = ["What does Contoso Travel offer?", "Explain travel insurance."]
    
    for query in queries:
        print(f"\nProcessing Query: {query}")
        result = await ask_rag(query, project_client, agent, evaluator)
        if result:
            print("Response:", result["response"])
            print("Metrics:", result["metrics"])
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    if asyncio.get_event_loop().is_running():
        await main()
    else:
        asyncio.run(main())
