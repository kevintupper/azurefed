# Graphlit helper functions for applicaiions using Streamlit

# Standard imports
import os
from dotenv import load_dotenv
import jwt

# Third-party imports
import streamlit as st

# SK imports
from graphlit_client import Graphlit


# Load environment variables locally if not on Azure, otherwise these will come from webapp config.
if not os.getenv("ON_AZURE"):
    load_dotenv(override=True)
 
# Assign the MSAL variables

GRAPHLIT_DOC_CHAT_PROJECT_ID=os.getenv("GRAPHLIT_DOC_CHAT_PROJECT_ID")
GRAPHLIT_API_URL=os.getenv("GRAPHLIT_API_URL")
GRAPHLIT_ORGANIZATION_ID=os.getenv("GRAPHLIT_ORGANIZATION_ID")
GRAPHLIT_PREVIEW_ENVIRONMENT_ID=os.getenv("GRAPHLIT_PREVIEW_ENVIRONMENT_ID")
GRAPHLIT_PREVIEW_ENVIRONMENT_SECRET=os.getenv("GRAPHLIT_PREVIEW_ENVIRONMENT_SECRET")


# Initialize a graphlit service
def initialize_graphlit_service():
    """
    Initialize a graphlit service.
    """

    # Only initialize if the graphlit service is not already initialized
    if "graphlit_initialized" not in st.session_state:
        
        # Setup the graphlit service session state variables        
        if 'graphlit_client' not in st.session_state:
            st.session_state['graphlit_client'] = None
        if 'graphlit_token' not in st.session_state:
            st.session_state['graphlit_token'] = None
        if 'graphlit_workflow_id' not in st.session_state:
            st.session_state['graphlit_workflow_id'] = None
        if 'graphlit_content_id' not in st.session_state:
            st.session_state['graphlit_content_id'] = None
        if 'graphlit_content_done' not in st.session_state:
            st.session_state['graphlit_content_done'] = None    
        if 'graphlit_specification_id' not in st.session_state:
            st.session_state['graphlit_specification_id'] = None
        if 'graphlit_conversation_id' not in st.session_state:
            st.session_state['graphlit_conversation_id'] = None
        if 'graphlit_environment_id' not in st.session_state:
            st.session_state['graphlit_environment_id'] = GRAPHLIT_PREVIEW_ENVIRONMENT_ID
        if 'graphlit_organization_id' not in st.session_state:
            st.session_state['graphlit_organization_id'] = GRAPHLIT_ORGANIZATION_ID
        if 'graphlit_secret_key' not in st.session_state:
            st.session_state['graphlit_secret_key'] = GRAPHLIT_PREVIEW_ENVIRONMENT_SECRET
        
        # Initialize the graphlit service and store the token in the session state
        st.session_state.graphlit_client = Graphlit(environment_id=GRAPHLIT_PREVIEW_ENVIRONMENT_ID, organization_id=GRAPHLIT_ORGANIZATION_ID, secret_key=GRAPHLIT_PREVIEW_ENVIRONMENT_SECRET)
        st.session_state.graphlit_token = st.session_state.graphlit_client.token
        
        print("Graphlit token generated successfully.")
    else:
        st.error("Failed to initialize the graphlit service. Please inform admin.")
        
        
# From Kirk's code

def ingest_file(name, mimeType, data):
    st.markdown(f"Ingesting [{name}], MIME type [{mimeType}]")

    # Define the GraphQL mutation
    mutation = """
    mutation IngestEncodedFile($name: String!, $mimeType: String!, $data: String!, $workflow: EntityReferenceInput, $isSynchronous: Boolean) {
        ingestEncodedFile(name: $name, mimeType: $mimeType, data: $data, workflow: $workflow, isSynchronous: $isSynchronous) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "isSynchronous": True, # wait for content to be ingested
        "name": name,
        "mimeType": mimeType,
        "data": data,
        "workflow": {
            "id": st.session_state['graphlit_workflow_id']
        }
    }

    # Convert the request to JSON format
    response = st.session_state['graphlit_client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['graphlit_content_id'] = response['data']['ingestEncodedFile']['id']

    return None


def delete_content():
    # Define the GraphQL mutation
    query = """
    mutation DeleteContent($id: ID!) {
        deleteContent(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['graphlit_content_id']
    }

    response = st.session_state['graphlit_client'].request(query=query, variables=variables)

def delete_all_contents():
    # Define the GraphQL mutation
    query = """
    mutation DeleteAllContents() {
        deleteAllContents() {
            id
            state
        }
        }
    """

    # Define the variables for the mutation
    variables = {
    }
    response = st.session_state['graphlit_client'].request(query=query, variables=variables)

def create_workflow():
    # Define the GraphQL mutation
    mutation = """
    mutation CreateWorkflow($workflow: WorkflowInput!) {
        createWorkflow(workflow: $workflow) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "workflow": {
            "preparation": {
                "jobs": [
                    {
                    "connector": {
                        "type": "AZURE_DOCUMENT_INTELLIGENCE",
                        "azureDocument": {
                            "model": "LAYOUT"
                        }
                    }
                    }
                ]
            },
            "name": "Azure AI Document Intelligence"
        }
    }

    # Convert the request to JSON format
    response = st.session_state['graphlit_client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['graphlit_workflow_id'] = response['data']['createWorkflow']['id']

    return None

def delete_workflow():
    # Define the GraphQL mutation
    query = """
    mutation DeleteWorkflow($id: ID!) {
        deleteWorkflow(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['graphlit_workflow_id']
    }
    response = st.session_state['graphlit_client'].request(query=query, variables=variables)

def create_specification():
    # Define the GraphQL mutation
    mutation = """
    mutation CreateSpecification($specification: SpecificationInput!) {
        createSpecification(specification: $specification) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "specification": {
            "type": "COMPLETION",
            "serviceType": "OPEN_AI",
            "searchType": "VECTOR",
            "openAI": {
                "model": "GPT4_TURBO_128K",
                "temperature": 0.1,
                "probability": 0.2,
                "completionTokenLimit": 2048
            },
            "strategy": { 
                "embedCitations": True,
            },
            "promptStrategy": { 
                "type": "OPTIMIZE_SEARCH" # rewrite for semantic search
            },
            # TODO: requires new PROD release
            "retrievalStrategy": {
                "type": "SECTION",
                "contentLimit": 10,
            },
#            "rerankingStrategy": {
#                "serviceType": "COHERE"
#            },
            "name": "Completion"
        }
    }

    # Convert the request to JSON format
    response = st.session_state['graphlit_client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['graphlit_specification_id'] = response['data']['createSpecification']['id']

    return None

def delete_specification():
    # Define the GraphQL mutation
    query = """
    mutation DeleteSpecification($id: ID!) {
        deleteSpecification(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['graphlit_specification_id']
    }
    response = st.session_state['graphlit_client'].request(query=query, variables=variables)

def create_conversation():
    # Define the GraphQL mutation
    mutation = """
    mutation CreateConversation($conversation: ConversationInput!) {
    createConversation(conversation: $conversation) {
        id
    }
    }
    """

    variables = {
        "conversation": {
            "specification": {
                "id": st.session_state['graphlit_specification_id']
            },
            # "filter": {
                # "contents":[
                #     {
                #         "id": st.session_state['graphlit_content_id']                        
                #     }
                # ]
            # },
            "name": "Conversation"
        }
    }

    # Send the GraphQL request with the JWT token in the headers
    response = st.session_state['graphlit_client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['graphlit_conversation_id'] = response['data']['createConversation']['id']

    return None

def delete_conversation():
    # Define the GraphQL mutation
    query = """
    mutation DeleteConversation($id: ID!) {
        deleteConversation(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['graphlit_conversation_id']
    }
    response = st.session_state['graphlit_client'].request(query=query, variables=variables)

def prompt_conversation(prompt):
    # Define the GraphQL mutation
    mutation = """
    mutation PromptConversation($prompt: String!, $id: ID) {
    promptConversation(prompt: $prompt, id: $id) {
        message {
            message
        }
    }
    }
    """

    # Define the variables for the mutation
    variables = {
        "prompt": prompt,
        "id": st.session_state['graphlit_conversation_id']
    }

    # Send the GraphQL request with the JWT token in the headers
    response = st.session_state['graphlit_client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return None, error_message

    message = response['data']['promptConversation']['message']['message']

    return message, None
