# Helper for Semantic kernel

# Imports

# Standard imports
import os
from dotenv import load_dotenv

# Third-party imports
import streamlit as st

# SK imports
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.contents.chat_history import ChatHistory


# Load environment variables locally if not on Azure, otherwise these will come from webapp config.
if not os.getenv("ON_AZURE"):
    load_dotenv(override=True)
 
# Assign the MSAL variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME_GPT_4 = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT_4")
AZURE_OPENAI_DEPLOYMENT_NAME_GPT_35_TURBO = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT_35_TURBO")

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
    chat_service = sk_oai.AzureChatCompletion(service_id=service_id, **chat_config)

    # Add the service to the kernel
    st.session_state.kernel.add_service(chat_service)
    
    # Initialize the chat settings
    chat_settings = st.session_state.kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
    chat_settings.max_tokens = 2000
    chat_settings.temperature = 0.7
    chat_settings.top_p = 0.8
    chat_settings.stream = True
    chat_settings.auto_invoke_kernel_functions = True
    
    # Initialize the chat history
    chat_history = ChatHistory()

    # Initialize the chat service function
    chat_function = st.session_state.kernel.create_function_from_prompt(
        prompt="""You are an AI chatbot that answers questions and helps people. You use clear, plain language without jargon.
        {{$chat_history}}{{$user_input}}""",
        function_name=f"chat_{service_id}",
        plugin_name=f"chat_{service_id}",
        prompt_execution_settings=chat_settings
    )
    
    print(f"Initialized {service_id} chat service")
    
    return chat_service, chat_settings, chat_history, chat_function


# Initialize the application chat services.
def initialize_chat_services():
    """
    Initialize the chat services for the application.
    """


    # Initialize not already initialized
    if "chat_services" not in st.session_state:


        # Initialize the kernel
        if "kernel" not in st.session_state:  
            st.session_state.kernel = sk.Kernel()


        # Initialize each chat service (deployment_name, base_url, service_id, api_key, api_version)
        services_to_initialize = {
            "gpt_4": (AZURE_OPENAI_DEPLOYMENT_NAME_GPT_4, AZURE_OPENAI_ENDPOINT, "gpt_4", AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION),
            "gpt_35_turbo": (AZURE_OPENAI_DEPLOYMENT_NAME_GPT_35_TURBO, AZURE_OPENAI_ENDPOINT, "gpt_35_turbo", AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION),
        }

        for service_name, params in services_to_initialize.items():
            service, settings, history, function = initialize_chat_service(*params)
            # Store these in session_state with the service_name as a key
            st.session_state[f"{service_name}_service"] = service
            st.session_state[f"{service_name}_settings"] = settings
            st.session_state[f"{service_name}_history"] = history
            st.session_state[f"{service_name}_function"] = function
        
        # Initialize the chat services list and active chat service
        st.session_state.chat_services = list(services_to_initialize.keys())
        st.session_state.active_chat_service = "gpt_4"

# Generate response
async def generate_response(response_holder, chat_function, chat_history, prompt):

    # Invoke the chat service with the user input
    answer = st.session_state.kernel.invoke_stream(chat_function, user_input=prompt, chat_history=chat_history)
    output = ""
    async for message in answer:
        output += str(message[0])
        response_holder.write(output)

    # Return the output
    return output
