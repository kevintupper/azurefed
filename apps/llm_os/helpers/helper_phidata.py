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
 
# Get the Azure OpenAI API keys
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Get the Regulations.gov API key
REGULATIONS_GOV_API_KEY = os.getenv("REGULATIONS_GOV_API_KEY")


#***********************************************************************************************
# Rulemaking Assistants
#***********************************************************************************************

rma_stakeholder = Assistant(
    llm=AzureOpenAIChat(model=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_OPENAI_ENDPOINT, azure_api_version=AZURE_OPENAI_API_VERSION, azure_deployment=AZURE_OPENAI_DEPLOYMENT),
    tools=[DuckDuckGo()],
    show_tool_calls=True,
    description="You are an expert regulatory analyst.",
    instructions=[
        'Review the rule the user provides and return a list of likely stakeholders who may be impacted by the rule.',
        'A stakeholder is any person, group, official, or organization that has an interest in the outcome of the rule.',
        'Return the list of stakeholders as a JSON object with the following format: {"stakeholders": ["stakeholder1", "stakeholder2", ...]}.',
    ],
)

research_editor = Assistant(
    name="Research Editor",
    description="You are a world-class researcher and your task is to generate a NYT cover story worthy research report.",
    instructions=[
        "You will be provided with a topic and a list of articles along with their summary and content.",
        "Carefully read each articles and generate a NYT worthy report that can be published as the cover story.",
        "Focus on providing a high-level overview of the topic and the key findings from the articles.",
        "Do not copy the content from the articles, but use the information to generate a high-quality report.",
        "Do not include any personal opinions or biases in the report.",
    ],
    markdown=True,
    # debug_mode=True,
)

#***********************************************************************************************