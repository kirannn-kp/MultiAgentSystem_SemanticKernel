from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from config import PROJECT_CONNECTION_STRING, SUBSCRIPTION_ID, RESOURCE_GROUP_NAME, PROJECT_NAME, ASSISTANT_ID

def create_ai_agent():
    """Uses an existing AI Agent in Azure AI Foundry and processes a user request."""
    credential = AzureCliCredential()
    project_client = AIProjectClient(
        subscription_id=SUBSCRIPTION_ID,
        resource_group_name=RESOURCE_GROUP_NAME,
        project_name=PROJECT_NAME,
        endpoint=PROJECT_CONNECTION_STRING,
        credential=credential
    )

    with project_client:
        # Retrieve the existing AI Agent
        agent = project_client.agents.get_agent(assistant_id=ASSISTANT_ID)
        print(f"✅ Retrieved AI Agent: {agent.id}")

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