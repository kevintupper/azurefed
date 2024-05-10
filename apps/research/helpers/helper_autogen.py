# AutoGen helper functions for applicaiions using Streamlit

# Standard imports
import os
from dotenv import load_dotenv

# Autogen imports
from autogen import ConversableAgent

# Third-party imports
import streamlit as st


# Load environment variables locally if not on Azure, otherwise these will come from webapp config.
if not os.getenv("ON_AZURE"):
    load_dotenv(override=True)
 
 
# Assign environment variables
AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION=os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME_GPT_4=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT_4")
AZURE_OPENAI_DEPLOYMENT_NAME_GPT_35_TURBO=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT_35_TURBO")

# Default LLM Config
DEFAULT_LLM_CONFIG = {
    "config_list": [
        {
            "model": AZURE_OPENAI_DEPLOYMENT_NAME_GPT_4,
            "api_key": AZURE_OPENAI_API_KEY,
            "api_type": "azure",
            "base_url": AZURE_OPENAI_ENDPOINT,
            "api_version": AZURE_OPENAI_API_VERSION,
            "tags": ["gpt-4"]
        },
        {
            "model": AZURE_OPENAI_DEPLOYMENT_NAME_GPT_35_TURBO,
            "api_key": AZURE_OPENAI_API_KEY,
            "api_type": "azure",
            "base_url": AZURE_OPENAI_ENDPOINT,
            "api_version": AZURE_OPENAI_API_VERSION,
            "tags": ["gpt-35-turbo"]
        }
#        {
#            "model": "llama-7B",
#            "base_url": "http://127.0.0.1:8080",
#            "api_type": "openai",
#        },
    ],
#    "temperature": 0.9,
#    "timeout": 300,
}


# Get Conversable Agent
def get_conversable_agent(config=DEFAULT_LLM_CONFIG):
    
    # Instantiate a ConversableAgent
    agent = ConversableAgent(
        "chatbot",
        llm_config=config,
        code_execution_config=False,    # Turn off code execution, by default it is off.
        function_map=None,              # No registered functions, by default it is None.
        human_input_mode="NEVER",       # Never ask for human input.
    )
    
    # Return the agent
    return agent