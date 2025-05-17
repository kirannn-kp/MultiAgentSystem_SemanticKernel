# Hydrogen Product Assistant (MultiAgent System eith Semantic)
Architecture Diagram

![Architecture Diagram](assets/architecture_diagram.png)

## Overview
The Hydrogen Product Assistant is an AI-powered application designed to assist users in searching for hydrogen-related products, generating detailed reports, and providing actionable guidance. The application integrates Azure Cognitive Search, Azure AI Services, and other tools to deliver a seamless user experience.

## Features
- **Search for Hydrogen Products**: Leverages Azure Cognitive Search to find hydrogen-related products based on user queries.
- **Generate Reports**: Creates detailed reports about hydrogen products using Azure AI Services.
- **Actionable Guidance**: Provides location-based guidance by opening Google Maps for queries like "Guide me to the nearest hydrogen producer in Frankfurt."
- **Web Search Fallback**: Uses Wikipedia as a fallback for web searches when no results are found in the local index.
- **Real-Time Audio Interaction**: Supports speech-to-text and text-to-speech for real-time audio-based interaction.

## Prerequisites
- Python 3.9 or later
- Azure Cognitive Search service
- Azure AI Services (e.g., Bing Web Search API)
- Google Chrome or any default web browser for map links

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/vector_aiAgent.git
   cd vector_aiAgent
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - `AZURE_SEARCH_ENDPOINT`: Your Azure Cognitive Search endpoint.
   - `AZURE_SEARCH_API_KEY`: Your Azure Cognitive Search API key.
   - `AZURE_OPENAI_RT_ENDPOINT`: Your Azure OpenAI endpoint.
   - `AZURE_OPENAI_RT_KEY`: Your Azure OpenAI API key.
   - `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID.
   - `AZURE_RESOURCE_GROUP_NAME`: Your Azure resource group name.
   - `AZURE_PROJECT_NAME`: Your Azure project name.
   - `ASSISTANT_ID`: Your Azure AI assistant ID.

## Usage
1. Start the application:
   ```bash
   python poc/main.py
   ```
2. Interact with the assistant:
   - **Search**: "Search for hydrogen producer in Berlin."
   - **Report**: "Generate a report for Hydrogen Generator A."
   - **Guidance**: "Guide me to the nearest hydrogen producer in Frankfurt."

## Project Structure
```
vector_aiAgent/
├── poc/
│   ├── agent.py               # Main logic for agents
│   ├── config.py              # Configuration settings
│   ├── main.py                # Entry point of the application
│   ├── reply.wav              # Sample audio file
│   ├── requirements.txt       # Python dependencies
│   ├── retrieval.py           # Retrieval logic
│   ├── speech_service.py      # Speech-to-text and text-to-speech services
│   ├── test_agent_connectivity.py # Test script for agent connectivity
│   └── __pycache__/           # Compiled Python files
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [Azure Cognitive Search](https://azure.microsoft.com/en-us/services/search/)
- [Azure AI Services](https://azure.microsoft.com/en-us/services/ai/)
- [Google Maps](https://www.google.com/maps)
