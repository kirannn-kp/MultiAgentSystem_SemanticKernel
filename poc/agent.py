import os
import requests  # Ensure the requests library is imported for web search functionality
from config import AZURE_OPENAI_RT_ENDPOINT, AZURE_OPENAI_RT_KEY, SUBSCRIPTION_ID, RESOURCE_GROUP_NAME, PROJECT_NAME, ASSISTANT_ID
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient  
from azure.core.credentials import AzureKeyCredential  
from azure.ai.projects import AIProjectClient  
from azure.identity import DefaultAzureCredential   
from azure.ai.projects.models import AzureAISearchTool, MessageTextContent, MessageTextDetails
from speech_service import speech_to_text, text_to_speech
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from semantic_kernel.functions.kernel_function import KernelFunction
import asyncio  
import webbrowser


kernel = Kernel()

kernel.services["azure-openai"] = AzureChatCompletion(
    endpoint=AZURE_OPENAI_RT_ENDPOINT,
    api_key=AZURE_OPENAI_RT_KEY,
    deployment_name="gpt-4-deployment"  
)


define_skill = KernelFunction.from_prompt(
    function_name="example_skill",
    plugin_name="example_plugin",
    description="A simple example skill",
    prompt="Processed input: {input_text}"
)

result = define_skill("Hello, Semantic Kernel!")
print(result)

def create_ai_agent():
    """Uses an existing AI Agent in Azure AI Foundry and processes a user request."""
    project_client = AIProjectClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID,
        resource_group_name=RESOURCE_GROUP_NAME,
        project_name=PROJECT_NAME,
        endpoint="https://swedencentral.api.azureml.ms"
    )

    agent = project_client.agents.get_agent(agent_id=ASSISTANT_ID)
    print(f"Retrieved AI Agent: {agent.id}")

    thread = project_client.agents.create_thread()
    print(f"Created Thread: {thread.id}")

    return project_client, agent, thread

class HydrogenSearchAgent:
    """
    A class to represent the Hydrogen Search Agent.
    """
    def ensure_index_exists(self):
        """
        Ensures that the Azure Cognitive Search index exists. If not, it creates the index.
        """
        print("Ensuring the Azure Cognitive Search index exists...")

        search_service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        search_service_api_key = os.getenv("AZURE_SEARCH_API_KEY")
        index_name = "hydrogen-products"


        index_client = SearchIndexClient(
            endpoint=search_service_endpoint,
            credential=AzureKeyCredential(search_service_api_key)
        )

 
        try:
            index_client.get_index(index_name)
            print(f"Index '{index_name}' already exists.")
        except Exception as e:
            print(f"Index '{index_name}' does not exist. Attempting to create it...")
            print(f"Error details: {e}")

            semantic_config = {
                "name": "default-semantic-config",
                "prioritizedFields": {
                    "titleField": {"fieldName": "name"},
                    "contentFields": [{"fieldName": "description"}],
                    "keywordsField": {"fieldName": "location"}
                }
            }

        
            index_schema = SearchIndex(
                name=index_name,
                fields=[
                    SimpleField(name="id", type="Edm.String", key=True),
                    SearchableField(name="name", type="Edm.String"),
                    SearchableField(name="description", type="Edm.String"),
                    SimpleField(name="location", type="Edm.String")
                ],
                semantic_settings={"configurations": [semantic_config]}  
            )

            try:
                index_client.create_index(index_schema)
                print(f"Index '{index_name}' created successfully.")
            except Exception as create_error:
                print(f"Failed to create index '{index_name}'. Error details: {create_error}")

            
            try:
                index_client.create_or_update_index(
                    SearchIndex(
                        name=index_name,
                        fields=[
                            SimpleField(name="id", type="Edm.String", key=True),
                            SearchableField(name="name", type="Edm.String"),
                            SearchableField(name="description", type="Edm.String"),
                            SimpleField(name="location", type="Edm.String")
                        ],
                        semantic_settings={
                            "configurations": [
                                {
                                    "name": "default-semantic-config",
                                    "prioritizedFields": {
                                        "titleField": {"fieldName": "name"},
                                        "contentFields": [{"fieldName": "description"}],
                                        "keywordsField": {"fieldName": "location"}
                                    }
                                }
                            ]
                        }
                    )
                )
                print(f"Semantic configuration applied to index '{index_name}'.")
            except Exception as semantic_error:
                print(f"Failed to apply semantic configuration. Error: {semantic_error}")

    def upload_sample_data(self):
        """
        Uploads sample data to the Azure Cognitive Search index.
        """
        print("Uploading sample data to the Azure Cognitive Search index...")

     
        search_service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        search_service_api_key = os.getenv("AZURE_SEARCH_API_KEY")
        index_name = "hydrogen-products"

  
        search_client = SearchClient(
            endpoint=search_service_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(search_service_api_key)
        )

        # Sample data to upload
        sample_data = [
            {
                "id": "1",
                "name": "Hydrogen Generator A",
                "description": "A compact hydrogen generator suitable for industrial use.",
                "location": "Frankfurt"
            },
            {
                "id": "2",
                "name": "Hydrogen Fuel Cell B",
                "description": "A high-efficiency hydrogen fuel cell for vehicles.",
                "location": "Berlin"
            },
            {
                "id": "3",
                "name": "Hydrogen Storage Tank C",
                "description": "A durable storage tank for hydrogen gas.",
                "location": "Munich"
            },
            {
                "id": "4",
                "name": "Hydrogen Solutions GmbH",
                "description": "Operates a large hydrogen production facility in Frankfurt am Main, producing green hydrogen via electrolysis.",
                "location": "Frankfurt"
            },
            {
                "id": "5",
                "name": "Frankfurt Hydrogen Center",
                "description": "Produces over 10 tons of hydrogen per day, serving industrial clients in the Rhine-Main region.",
                "location": "Frankfurt"
            }
        ]

        try:
            result = search_client.upload_documents(documents=sample_data)
            print(f"Uploaded {len(result)} documents to the index '{index_name}'.")
        except Exception as e:
            print(f"Failed to upload sample data. Error: {e}")

    def search_hydrogen_products(self, product_name: str) -> str:
        """
        Searches for hydrogen products in Azure AI Search.

        Parameters:
        product_name (str): The name of the hydrogen product to search for.

        Returns:
        str: The search results in JSON format.
        """
        print("Calling HydrogenSearchAgent...")


        self.ensure_index_exists()

       
        project_client = AIProjectClient(
            credential=DefaultAzureCredential(),
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group_name=os.getenv("AZURE_RESOURCE_GROUP_NAME"),
            project_name=os.getenv("AZURE_PROJECT_NAME"),
            endpoint=os.getenv("PROJECT_CONNECTION_STRING")
        )

      
        conn_list = project_client.connections.list()
        conn_id = ""
        for conn in conn_list:
            if conn.connection_type == "CognitiveSearch":
                conn_id = conn.id

        ai_search = AzureAISearchTool(index_connection_id=conn_id, index_name="hydrogen-products")

        search_agent = project_client.agents.create_agent(
            model="gpt-4o",
            name="hydrogen-search-agent",
            instructions="You are an expert in searching for hydrogen products.",
            tools=ai_search.definitions,
            tool_resources=ai_search.resources,
        )

 
        thread = project_client.agents.create_thread()

    
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=f"Find details about the hydrogen product: {product_name}.",
        )

    
        run = project_client.agents.create_and_process_run(
            thread_id=thread.id,
            agent_id=search_agent.id  
        )

 
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")

        project_client.agents.delete_agent(search_agent.id)


        messages = project_client.agents.list_messages(thread_id=thread.id)

        last_msg = messages.get_last_text_message_by_role("assistant")

        print("HydrogenSearchAgent completed successfully.")

        return last_msg

def hydrogen_search_skill(product_name: str) -> str:
    search_agent = HydrogenSearchAgent()
    return search_agent.search_hydrogen_products(product_name)

kernel.services["hydrogen-search-skill"] = hydrogen_search_skill


class HydrogenOrchestratorAgent:
    """
    A class to represent the Hydrogen Orchestrator Agent.
    """
    def __init__(self):
        self.kernel = kernel  

    async def orchestrate(self, user_input: str) -> str:
        """
        Orchestrates the communication between agents based on user input.

        Parameters:
        user_input (str): The user's input or query.

        Returns:
        str: The final response after orchestrating the agents.
        """
        print("Orchestrating agents with Semantic Kernel...")

        user_lower = user_input.lower()
        if "search" in user_lower:
            product_name = user_input.replace("search", "").strip()
            search_results = self.kernel.services["hydrogen-search-skill"](product_name)
            return str(search_results).strip()
        elif "report" in user_lower:
            report_query = user_input.replace("report", "").strip()
            report_agent = HydrogenReportAgent()
            product_name = report_query  
            product_info = "Detailed information about the product."
            return report_agent.generate_report(product_name, product_info)
        elif "guidance" in user_lower:
            guidance_query = user_input.replace("guidance", "").strip()
       
            guidance_agent = HydrogenGuidanceAgent()
            return guidance_agent.provide_guidance(guidance_query)

        return "Invalid input. Please specify 'search', 'report', or 'guidance' in your query."

class HydrogenReportAgent:
    """
    A class to represent the Hydrogen Report Agent.
    """
    def generate_report(self, product_name: str, product_info: str) -> str:
        """
        Generates a detailed report about a hydrogen product.

        Parameters:
        product_name (str): The name of the hydrogen product.
        product_info (str): The information about the hydrogen product.

        Returns:
        str: The generated report.
        """
        print("Calling HydrogenReportAgent...")


        project_client = AIProjectClient(
            credential=DefaultAzureCredential(),
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group_name=os.getenv("AZURE_RESOURCE_GROUP_NAME"),
            project_name=os.getenv("AZURE_PROJECT_NAME"),
            endpoint=os.getenv("PROJECT_CONNECTION_STRING")
        )

        report_agent = project_client.agents.create_agent(
            model="gpt-4o",
            name="hydrogen-report-agent",
            instructions="You are an expert in generating detailed reports about hydrogen products.",
        )


        thread = project_client.agents.create_thread()

   
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=f"Generate a detailed report about the hydrogen product: {product_name}. Here is the information: {product_info}.",
        )


        run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=report_agent.id)

        if run.status == "failed":
            print(f"Run failed: {run.last_error}")


        project_client.agents.delete_agent(report_agent.id)
        messages = project_client.agents.list_messages(thread_id=thread.id)
        last_msg = messages.get_last_text_message_by_role("assistant")

        print("HydrogenReportAgent completed successfully.")

        return last_msg

class HydrogenGuidanceAgent:
    """
    A class to represent the Hydrogen Guidance Agent.
    """
    def provide_guidance(self, user_query: str) -> str:
        """
        Provides guidance based on user queries, including actionable map links for location-based queries.

        Parameters:
        user_query (str): The user's query.

        Returns:
        str: The guidance provided by the agent, including map links if applicable.
        """
        print("Calling HydrogenGuidanceAgent...")

        # Example: Extract location from query
        if "nearest hydrogen producer" in user_query.lower():
            location = user_query.split("in")[-1].strip()
            print(f"Extracted location: {location}")

            # Generate a Google Maps link for the location
            maps_url = f"https://www.google.com/maps/search/?api=1&query=hydrogen+producer+in+{location}"

            # Open the link in the default web browser
            webbrowser.open(maps_url)

            return f"Opening the location of the nearest hydrogen producer in {location} on your browser: {maps_url}"

        # Default behavior for other guidance queries
        return "I'm sorry, I can only provide location-based guidance for now."

class WebSearchAgent:
    """
    Agent to perform external web searches when local index is insufficient.
    """
    def search_web(self, query: str) -> str:
        """Performs a simple Wikipedia-based web search and returns key snippets."""
        try:
            resp = requests.get(
                'https://en.wikipedia.org/w/api.php',
                params={
                    'action': 'opensearch',
                    'search': query,
                    'limit': 3,
                    'format': 'json'
                }, timeout=5
            )
            data = resp.json()
            titles, descriptions, links = data[1], data[2], data[3]
            results = [f"{t}: {d} ({l})" for t, d, l in zip(titles, descriptions, links)]
            return "\n".join(results) or "No web results found."
        except Exception as e:
            return f"Web search failed: {e}"

class ResponseAggregatorAgent:
    """
    Aggregates outputs from multiple agents into a single response.
    """
    def aggregate(self, search_output: str, web_output: str) -> str:
        return (
            "Aggregated Response:\n"
            f"1) Search Agent Output:\n{search_output}\n\n"
            f"2) Web Agent Output:\n{web_output}\n"
        )

class RealTimeAudioAgent:
    """
    Uses speech-to-text and text-to-speech services for real-time audio interaction via the orchestrator.
    """
    def __init__(self):
        print("RealTimeAudioAgent initialized.")

        self.orchestrator = HydrogenOrchestratorAgent()

    async def converse(self):
        print("Starting real-time audio session. Say 'stop' to quit.")
        while True:
            print("Listening for user speech...")
            user_text = speech_to_text()
            if not user_text:
                print("No speech detected. Please try again.")
                continue
            if user_text.strip().lower() in ("stop", "exit", "quit"):
                print("Ending audio session.")
                break
            print(f"User said: {user_text}")

            response = await self.orchestrator.orchestrate(user_text)
            print(f"Assistant: {response}")
            text_to_speech(response)

            # Ensure text-to-speech completes before resuming listening
            await asyncio.sleep(2)
