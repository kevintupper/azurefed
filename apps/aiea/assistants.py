# Phidata imports
from phi.assistant import Assistant
from phi.llm.azure import AzureOpenAIChat

from helpers import helper_phidata as helper_phidata



#***********************************************************************************************
# Assistants
#***********************************************************************************************


# Outliner
def get_outliner_assistant(content_type, topic, target_audience, tone_style, content_length, ideas_to_include):
    """
    Creates an assistant tailored to generate content outlines based on given parameters.
    
    :param content_type: The type of content to generate (e.g., 'Video Talk Track', 'LinkedIn Article').
    :param topic: Specific topic for the content.
    :param target_audience: Description of the target audience.
    :param tone_style: Desired tone and style of the content.
    :param content_length: Expected length and detail level of the content.
    :param ideas_to_include: Key points or ideas that must be included in the content.
    :param resources: Resources to be considered or cited in the content.
    :return: Configured Assistant instance.
    """
    description = f"You are a world-class outline creator for {content_type.lower()}"
    instructions = ["**Topic**", topic, "**Target Audience**", target_audience, "**Tone/Style**", tone_style, "**Content Length**", content_length, "**Key Ideas to Include**", ideas_to_include,"Format the outline clearly and logically."]

    outliner_assistant = Assistant(
        llm=AzureOpenAIChat(model=helper_phidata.AZURE_OPENAI_API_KEY, azure_endpoint=helper_phidata.AZURE_OPENAI_ENDPOINT, azure_api_version=helper_phidata.AZURE_OPENAI_API_VERSION, azure_deployment=helper_phidata.AZURE_OPENAI_DEPLOYMENT_NAME),
        description=description,
        instructions=instructions
    )
    
    return outliner_assistant

