from agent import  RealTimeAudioAgent
from speech_service import  text_to_speech
import asyncio

async def process_user_response(project_client, agent, thread, user_input):
    """Processes user choice and continues conversation accordingly."""
    user_input = user_input.strip().lower()  # Normalize input

    # Predefined questions and their responses
    predefined_responses = {
        "where is the nearest hydrogen producer": "The nearest hydrogen producer in Mannheim is XYZ Energy.",
        "where is the nearest hydrogen producer in germany": "The nearest hydrogen producer in Germany is located in Mannheim, operated by XYZ Energy.",
        "what is hydrogen energy": "Hydrogen energy is a clean and renewable energy source produced by splitting water into hydrogen and oxygen.",
        "hello, what is your name?": "My name is GitHub Copilot. How can I assist you today?"
    }

    normalized_predefined_responses = {
        key.strip().lower(): value for key, value in predefined_responses.items()
    }

    print(f"Debug: Normalized User Input: {user_input}")

    for question, response in normalized_predefined_responses.items():
        if all(keyword in user_input for keyword in question.split()):
            print(f"Matched Predefined Response: {response}")
            return response
    print("No predefined response found for the input.")
    return "I'm sorry, I don't have an answer for that question."


async def main():
    """
    Entry point for the Hydrogen Orchestrator System.
    """
    from agent import HydrogenOrchestratorAgent
    orchestrator = HydrogenOrchestratorAgent()
    audio_agent = RealTimeAudioAgent()

    is_audio_mode = False  # Flag to track audio mode

    print("Welcome to the Hydrogen Product Assistant!")
    print("You can ask me to 'search' for hydrogen products, 'report' on a product, or provide 'guidance'.")
    print("Type 'audio' to start a real-time audio session, or type your query directly.")

    while True:
        user_input = input("\n> ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Exiting the assistant. Goodbye!")
            break

        if user_input.lower() == "audio":
            is_audio_mode = True
            await audio_agent.converse()
            is_audio_mode = False  
        else:

            response = await orchestrator.orchestrate(user_input)
            print(f"Assistant: {response}")
            if is_audio_mode:
                text_to_speech(response)


if __name__ == "__main__":
    asyncio.run(main())