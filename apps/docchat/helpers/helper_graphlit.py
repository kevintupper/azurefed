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
        
        # Initialize the graphlit service and store the token in the session state
        st.session_state.graphlit_client = Graphlit(environment_id=GRAPHLIT_PREVIEW_ENVIRONMENT_ID, organization_id=GRAPHLIT_ORGANIZATION_ID, secret_key=GRAPHLIT_PREVIEW_ENVIRONMENT_SECRET)
        st.session_state.graphlit_token = st.session_state.graphlit_client.token
        print("Graphlit token generated successfully.")
    else:
        st.error("Failed to initialize the graphlit service. Please inform admin.")