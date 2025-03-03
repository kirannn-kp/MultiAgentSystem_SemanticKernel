import asyncio
from azure.ai.projects import AIProjectClient
from config import ASSISTANT_ID
from agent import create_ai_agent
from evaluator import RAGEvaluator

async def process_user_response(project_client: AIProjectClient, agent, thread, user_choice):
    """Processes user choice and continues conversation accordingly."""
    if user_choice == "Yes":
        response_text = "Here is the link: [Hydrogen Producer Info](https://example.com)"
    elif user_choice.startswith("Option"):
        response_text = f"You selected {user_choice}. Would you like more details?"
    else:
        response_text = "Thank you! Let me know if you need anything else."

    message = project_client.agents.create_message(thread_id=thread.id, role="assistant", content=response_text)
    print(f"✅ Sent Response: {message.id}")

async def main():
    """Runs the full chatbot interaction."""
    project_client, agent, thread = create_ai_agent()
    evaluator = RAGEvaluator()

    user_input = input("Enter your choice: ")  # Simulate user response for testing
    await process_user_response(project_client, agent, thread, user_input)

if __name__ == "__main__":
    if asyncio.get_event_loop().is_running():
        asyncio.create_task(main())
    else:
        asyncio.run(main())
