# helper_auth

# Import required libraries
import msal
import requests
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables locally if not on Azure, otherwise these will come from webapp config.
if not os.getenv("ON_AZURE"):
    load_dotenv(override=True)
 
# Assign the MSAL variables
MSAL_CLIENT_ID = os.getenv("MSAL_CLIENT_ID")
MSAL_TENANT_ID = os.getenv("MSAL_TENANT_ID")
MSAL_CLIENT_SECRET = os.getenv("MSAL_CLIENT_SECRET")
MSAL_SCOPES = os.getenv("MSAL_SCOPES").split(',') if os.getenv("MSAL_SCOPES") else []
MSAL_REDIRECT_URI = os.getenv("MSAL_REDIRECT_URI")
MSAL_AUTHORITY = os.getenv("MSAL_AUTHORITY") 


# Initialize the MSAL ConfidentialClientApplication with the required credentials
app = msal.ConfidentialClientApplication(
    client_id=MSAL_CLIENT_ID, 
    authority=MSAL_AUTHORITY, 
    client_credential=MSAL_CLIENT_SECRET
)

# Initialize the user ino in the session state
st.session_state["user_info"] = None

def get_auth_url():
    """
    Generate the authorization URL for the user to sign in.
    """
    auth_url = app.get_authorization_request_url(scopes=MSAL_SCOPES, redirect_uri=MSAL_REDIRECT_URI)
    return auth_url


def get_token_from_code(auth_code):
    """
    Retrieve the token from the authorization code.
    """
    try:
        result = app.acquire_token_by_authorization_code(auth_code, scopes=MSAL_SCOPES, redirect_uri=MSAL_REDIRECT_URI)
        return result["access_token"]
    except Exception as err:
        return ""

# def get_tid_from_token(access_token):
#     """
#     Decode the JWT access token to extract the tenant ID (tid) claim.
#     """
#     decoded_token = jwt.decode(access_token, options={"verify_signature": False})
#     return decoded_token.get("tid")


def get_user_info(access_token):
    """
    Retrieve user information from the Microsoft Graph API using the access token.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
    return response.json()


def enforce_authentication():
    """
    Ensure the user is authenticated by processing the authentication response, storing the access token and user information in the session state.
    """
    if not st.session_state.get("access_token"):
        # Get the query parameters
        qp = st.query_params.to_dict()
        if qp:
            # Get the access token from the query parameters
            access_token = get_token_from_code(qp["code"])
            
            # Make sure the access token is not empty
            if access_token:

                # Store the access token in the session_state
                st.session_state["access_token"] = access_token
                st.query_params.access_token = access_token

                # NO LONGER NEEDED - WE ARE USING A SINGLE TENANT WITH APP REGISTRATION ON MSFT
                # # Extract tenant ID from the token
                # tenant_id = get_tid_from_token(access_token)
                # if tenant_id not in MSAL_ALLOWED_TENANTS:
                #     # Handle unauthorized tenant
                #     st.error("Access denied. Your account does not belong to an authorized domain.")
                #     return

                user_info = get_user_info(access_token)
                if user_info:
                    st.session_state["user_info"] = user_info
                    # Clear the query parameters
                    st.query_params.clear()
                else:
                    # Handle error: user info could not be acquired
                    st.error("Failed to retrieve user information.")
            else:
                # Handle error: access token could not be acquired
                st.error("Authentication failed.")

            # Initialize user settings upon successful authentication
            #user_settings.init_settings()


def display_sign_in_screen(title="Microsoft", subtitle="Federal Demo Platform", message="Welcome to the Microsoft Federal Demo Platform. Please sign-in with an authorized account."):
    """
    Display the sign-in screen to the user.
    """

    # Display the title and subtitle
    st.title(title)
    st.subheader(subtitle)

    # Display a message to the user to sign in
    st.write(message)

    # Get the authentication URL
    auth_url = get_auth_url()

    # Display the sign-in button to the user
    st.markdown(f"""
        <style>
            .signin-button {{
                background-color: teal;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 18px;
                margin: 4px 2px;
                cursor: pointer;
            }}
        </style>
        <a href='{auth_url}' target='_self'><button class='signin-button'>Sign In</button></a>
        """, unsafe_allow_html=True)


def get_user_id(user_info=st.session_state["user_info"]):
    """
    Get the user ID from the user information and return it if present.
    """
    return user_info["id"]


def get_user_email(user_info):
    """
    Get the user email from the user information.
    """
    return user_info["mail"]


def get_user_alias(user_info):
    """
    Get the user email from the user information.
    """
    try:
        return user_info["userPrincipalName"].split("@")[0]
    except:
        return ""


def get_user_display_name(user_info):
    """
    Get the user email from the user information.
    """
    return user_info["displayName"]


def get_user_job_title(user_info):
    """
    Get the user email from the user information.
    """
    return user_info["jobTitle"]


def get_user_office_location(user_info):
    """
    Get the user email from the user information.
    """
    return user_info["officeLocation"]


def get_user_given_name(user_info):
    """
    Get the user email from the user information.
    """
    return user_info["givenName"]
