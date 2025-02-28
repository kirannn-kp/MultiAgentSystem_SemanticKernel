from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from config import PROJECT_CONNECTION_STRING, AZURE_CREDENTIAL
from pathlib import Path

def create_ai_agent():
    """Creates an AI Agent in Azure AI Foundry and processes a user request."""
    project_client = AIProjectClient.from_connection_string(
        credential=AZURE_CREDENTIAL, conn_str=PROJECT_CONNECTION_STRING
    )

    with project_client:
        # Initialize tools
        code_interpreter = CodeInterpreterTool()

        # Create the AI Agent
        agent = project_client.agents.create_agent(
            model="gpt-4o-mini",
            name="retrieval-agent",
            instructions="You are an AI assistant that answers questions using ONLY the retrieved context.",
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
        )
        print(f"✅ Created AI Agent: {agent.id}")

        # Create a thread for the conversation
        thread = project_client.agents.create_thread()
        print(f"✅ Created Thread: {thread.id}")

        # Send a user message
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content="What are the advantages of cloud computing?",
        )
        print(f"✅ Sent Message: {message.id}")

        # Run the AI agent
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
        print(f"🔄 Run Status: {run.status}")

        # Handle errors
        if run.status == "failed":
            print(f"❌ Run failed: {run.last_error}")

        # Retrieve messages
        messages = project_client.agents.list_messages(thread_id=thread.id)
        last_msg = messages.get_last_text_message_by_role("assistant")

        if last_msg:
            print(f"🤖 AI Response: {last_msg.text.value}")

        # Save any generated image files
        for image_content in messages.image_contents:
            file_name = f"{image_content.image_file.file_id}_image_file.png"
            project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
            print(f"🖼️ Saved Image File: {file_name}")

        return project_client, agent  # Return for further usage if needed
