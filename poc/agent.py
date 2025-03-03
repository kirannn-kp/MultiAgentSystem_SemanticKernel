from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from config import PROJECT_CONNECTION_STRING, SUBSCRIPTION_ID, RESOURCE_GROUP_NAME, PROJECT_NAME, ASSISTANT_ID

ADAPTIVE_CARD_TEMPLATE = {
    "type": "AdaptiveCard",
    "version": "1.3",
    "body": [
        {"type": "TextBlock", "text": "{question}", "wrap": True},
        {
            "type": "ActionSet",
            "actions": [
                {"type": "Action.Submit", "title": "{option1}", "data": {"choice": "{option1}"}},
                {"type": "Action.Submit", "title": "{option2}", "data": {"choice": "{option2}"}}
            ]
        }
    ]
}

QUESTIONS = {
    "nearest_hydrogen_producer": {
        "question": "Where is the nearest hydrogen producer in Mannheim?",
        "options": ["Option 1: XYZ Energy", "Option 2: ABC Hydrogen"]
    },
    "get_link": {
        "question": "Do you want a link to more details?",
        "options": ["Yes", "No"]
    }
}

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
        agent = project_client.agents.get_agent(assistant_id=ASSISTANT_ID)
        print(f"✅ Retrieved AI Agent: {agent.id}")

        thread = project_client.agents.create_thread()
        print(f"✅ Created Thread: {thread.id}")

        question_key = "nearest_hydrogen_producer"
        adaptive_card = ADAPTIVE_CARD_TEMPLATE.copy()
        adaptive_card["body"][0]["text"] = QUESTIONS[question_key]["question"]
        adaptive_card["body"][1]["actions"][0]["title"] = QUESTIONS[question_key]["options"][0]
        adaptive_card["body"][1]["actions"][1]["title"] = QUESTIONS[question_key]["options"][1]

        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="assistant",
            content="Please choose an option:",
            attachments=[{"contentType": "application/vnd.microsoft.card.adaptive", "content": adaptive_card}]
        )
        print(f"✅ Sent Adaptive Card Message: {message.id}")

        return project_client, agent, thread
