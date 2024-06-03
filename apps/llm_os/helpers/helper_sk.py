# Helper for Semantic kernel

# Imports

# Standard imports
import os
from dotenv import load_dotenv

# Third-party imports
import streamlit as st

# SK imports
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_aoai
from semantic_kernel.contents.chat_history import ChatHistory


# Load environment variables locally if not on Azure, otherwise these will come from webapp config.
if not os.getenv("ON_AZURE"):
    load_dotenv(override=True)
 
# Assign the SK environment variables
LLM_OS_AOAI_API_KEY = os.getenv("LLM_OS_AOAI_API_KEY")
LLM_OS_AOAI_ENDPOINT = os.getenv("LLM_OS_AOAI_ENDPOINT")
LLM_OS_AOAI_API_VERSION = os.getenv("LLM_OS_AOAI_API_VERSION")
LLM_OS_AOAI_GPT4_DEPLOYMENT = os.getenv("LLM_OS_AOAI_GPT4_DEPLOYMENT")
LLM_OS_AOAI_GPT4o_DEPLOYMENT = os.getenv("LLM_OS_AOAI_GPT4o_DEPLOYMENT")
LLM_OS_AOAI_EMBEDDING_DEPLOYMENT = os.getenv("LLM_OS_AOAI_EMBEDDING_DEPLOYMENT")
LLM_OS_AOAI_DALLE3_DEPLOYMENT = os.getenv("LLM_OS_AOAI_DALLE3_DEPLOYMENT")

# Return a new chat history
def new_chat_history():
    """
    Return a new chat history.
    """
    return ChatHistory()


# Initialize a chat service
def initialize_chat_service(deployment_name, base_url, service_id, api_key, api_version):
    """
    Initialize a chat service.
    Parameters:
        deployment_name (str): The deployment name.
        base_url (str): The base URL.
        service_id (str): The service ID.
        api_key (str): The API key.
        api_version (str): The API version.
    """

    # Initialize the chat service
    chat_config = {"api_key": api_key, "endpoint": base_url, "deployment_name": deployment_name, "api_version": api_version}
    chat_service = sk_aoai.AzureChatCompletion(service_id=service_id, **chat_config)
    
    # Add the service to the kernel
    st.session_state.kernel.add_service(chat_service)

    print(f"Initialized {service_id} chat service")
    
    return chat_service


# Initialize the application chat services.
def initialize_chat_services():
    """
    Initialize the application chat services.

    Steps:
    - Initialize the kernel if not already initialized
    - Initialize each chat service
    - Store these in session_state with the service_name as a key
    - Initialize the chat services list and active chat service

    Session State Variables for Chat Services:
    - chat_services: The list of chat services
    - kernel: The kernel
    - {service_name}_service: The chat service for the service_name
    """

    # Initialize not already initialized
    if "chat_services" not in st.session_state:

        # Initialize the kernel
        if "kernel" not in st.session_state:  
            st.session_state.kernel = sk.Kernel()

        # Initialize each chat service (deployment_name, base_url, service_id, api_key, api_version)
        services_to_initialize = {
            "GPT 4": (LLM_OS_AOAI_GPT4_DEPLOYMENT, LLM_OS_AOAI_ENDPOINT, "gpt_4", LLM_OS_AOAI_API_KEY, LLM_OS_AOAI_API_VERSION),
            "GPT 4o": (LLM_OS_AOAI_GPT4o_DEPLOYMENT, LLM_OS_AOAI_ENDPOINT, "gpt_4o", LLM_OS_AOAI_API_KEY, LLM_OS_AOAI_API_VERSION),
        }

        # Store these in session_state with the service_name as a key
        for service_name, params in services_to_initialize.items():
            service = initialize_chat_service(*params)
            st.session_state[f"{service_name}_service"] = service
        
        # Initialize the chat services list set the active chat service
        st.session_state.chat_services = list(services_to_initialize.keys())
        st.session_state.active_chat_service_index = 1

# Generate streaming response
async def generate_streaming_response(response_holder, chat_service, system_message, chat_history, user_input, **kwargs):

    # Initialize the chat settings based on the service ID and kwargs
    service_id = chat_service.service_id
    chat_settings = sk_aoai.AzureChatPromptExecutionSettings(
        service_id=service_id,
        max_tokens=kwargs.get("max_tokens", 2000),
        temperature=kwargs.get("temperature", 0.7),
        top_p=kwargs.get("top_p", 0.8),
        frequency_penalty=kwargs.get("frequency_penalty", 0.0),
        presence_penalty=kwargs.get("presence_penalty", 0.0),
        stream=True,
    )
    
    
    # Build the chat history based on the system message and user input
    
    # If no chat history is provided, create a new one
    if not chat_history:
        chat_history = new_chat_history()
        
    # Add the user input to the chat history
    if user_input:
        chat_history.add_user_message(user_input)
        
    # If system message is provided, initialize the chat for the prompt with it and the chat history, otherwise just the chat history
    if system_message:
        chat = ChatHistory(messages=chat_history.messages, system_message=system_message)
    else:
        chat = chat_history

    # Execute the prompt 
    output = ""
    stream = chat_service.complete_chat_stream(chat_history=chat, settings=chat_settings)

    # Stream the response
    async for message in stream:
        output += str(message[0])
        response_holder.write(output)

    # Return the output
    return output


# Generate a response
async def generate_response(response_holder, chat_service, system_message, chat_history, user_input, **kwargs):
    
    # Initialize the chat settings based on the service ID and kwargs
    service_id = chat_service.service_id
    chat_settings = sk_aoai.AzureChatPromptExecutionSettings(
        service_id=service_id,
        max_tokens=kwargs.get("max_tokens", 2000),
        temperature=kwargs.get("temperature", 0.0),
        top_p=kwargs.get("top_p", 0.2),
        frequency_penalty=kwargs.get("frequency_penalty", 0.0),
        presence_penalty=kwargs.get("presence_penalty", 0.0),
        stream=False,  # Set stream to False for non-streaming execution
    )
    
    # Build the chat history based on the system message and user input
    
    # If no chat history is provided, create a new one
    if not chat_history:
        chat_history = new_chat_history()
        
    # Add the user input to the chat history
    if user_input:
        chat_history.add_user_message(user_input)
        
    # If system message is provided, initialize the chat for the prompt with it and the chat history, otherwise just the chat history
    if system_message:
        chat = ChatHistory(messages=chat_history.messages, system_message=system_message)
    else:
        chat = chat_history
        
    # Await the completion of the chat
    completions = await chat_service.complete_chat(chat_history=chat, settings=chat_settings)

    # Use the concatenated response
    response_holder.write(completions[0].content)
 
    return completions[0].content
        
