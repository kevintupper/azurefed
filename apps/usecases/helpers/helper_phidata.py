# Helper for Phidata
# https://docs.phidata.com/

# Imports

# Standard imports
import os
from dotenv import load_dotenv

# Third-party imports
import streamlit as st

# Phidata imports
from phi.assistant import Assistant
from phi.llm.azure import AzureOpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k

# Load environment variables locally if not on Azure, otherwise these will come from webapp config.
if not os.getenv("ON_AZURE"):
    load_dotenv(override=True)
 
# Assign the MSAL variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def get_assistant():
    assistant = Assistant(
    llm=AzureOpenAIChat(model=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_OPENAI_ENDPOINT, azure_api_version=AZURE_OPENAI_API_VERSION, azure_deployment=AZURE_OPENAI_DEPLOYMENT),
        tools=[DuckDuckGo(), Newspaper4k()],
        show_tool_calls=True,
        description="You are a senior NYT researcher writing an article on a topic.",
        instructions=[
            "For the provided topic, search for the top 3 links.",
            "Then read each URL and extract the article text, if a URL isn't available, ignore and let it be.",
            "Analyse and prepare an NYT worthy article based on the information.",
        ],
        add_datetime_to_instructions=True,
    )

    return assistant