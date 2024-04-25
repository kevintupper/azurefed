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

# Load environment variables locally if not on Azure, otherwise these will come from webapp config.
if not os.getenv("ON_AZURE"):
    load_dotenv(override=True)
 
# Assign the MSAL variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

def run_assistant():
    assistant = Assistant(
        llm=AzureOpenAIChat(model=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_OPENAI_ENDPOINT, azure_api_version=AZURE_OPENAI_API_VERSION, azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME),
        description="You help people with their health and fitness goals.",
    )
    assistant.print_response("Share a quick healthy breakfast recipe.", markdown=True)
