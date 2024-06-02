# Imports

# Standard imports
import os
from dotenv import load_dotenv

# Third-party imports
# import streamlit as st

# Phidata imports
from phi.assistant import Assistant
from phi.llm.azure import AzureOpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k

# Load environment variables locally if not on Azure, otherwise these will come from webapp config.
if not os.getenv("ON_AZURE"):
    load_dotenv(override=True)
 
# Get the Azure OpenAI API keys
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Get the Regulations.gov API key
REGULATIONS_GOV_API_KEY = os.getenv("REGULATIONS_GOV_API_KEY")

from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo


aoai_llm=AzureOpenAIChat(model=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_OPENAI_ENDPOINT, azure_api_version=AZURE_OPENAI_API_VERSION, azure_deployment=AZURE_OPENAI_DEPLOYMENT)
assistant = Assistant(llm=aoai_llm,tools=[DuckDuckGo()], show_tool_calls=True)
assistant.print_response("What is the current score of the Yankees game?", markdown=True)

