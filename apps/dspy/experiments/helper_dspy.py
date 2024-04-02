# Helper for DSPy

# Imports

# Standard imports
import os
from dotenv import load_dotenv

# Third-party imports
import streamlit as st

# DSPy imports
import dspy


# Load environment variables locally if not on Azure, otherwise these will come from webapp config.
if not os.getenv("ON_AZURE"):
    load_dotenv(override=True)
 
# Assign the MSAL variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME_GPT_4 = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT_4")
AZURE_OPENAI_DEPLOYMENT_NAME_GPT_35_TURBO = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT_35_TURBO")


# Return a DSPy client for the given service
def get_dspy_client(service_id, **kwargs):
    """
    Get a DSPy client for the given service.
    Parameters:
        service_id (str): The service ID.
    Returns:
        DSPy client
    """

    # Initialize the DSPy client
    if service_id == "gpt_4":
        client = dspy.AzureOpenAI(
            api_base=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY, 
            deployment_id=AZURE_OPENAI_DEPLOYMENT_NAME_GPT_4,
            api_version=AZURE_OPENAI_API_VERSION,
            **kwargs
        )
    elif service_id == "gpt_35_turbo":
        client = dspy.AzureOpenAI(
            api_base=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY, 
            deployment_id=AZURE_OPENAI_DEPLOYMENT_NAME_GPT_35_TURBO,
            api_version=AZURE_OPENAI_API_VERSION,
            **kwargs
        )
    else:
        raise ValueError(f"Service ID {service_id} not recognized")

    return client

