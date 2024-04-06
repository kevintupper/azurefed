# Storage helper functions for applicaiions using Streamlit

# Standard imports
import os
from dotenv import load_dotenv
from io import BytesIO
from datetime import datetime

# Third-party imports
import streamlit as st

# Storage imports
from azure.storage.blob import BlobServiceClient, ContainerClient


# Load environment variables locally if not on Azure, otherwise these will come from webapp config.
if not os.getenv("ON_AZURE"):
    load_dotenv(override=True)
 
# Assign the MSAL variables

AZURE_STORAGE_CONNECTION_STRING=os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER=os.getenv("AZURE_STORAGE_CONTAINER")


#********************************************************************************************************************
# Functions for storing and retrieving data from Azure Blob Storage
#********************************************************************************************************************
def get_blob_service_client() -> BlobServiceClient:
    """Create and return a BlobServiceClient instance using the connection string from credentials."""
    return BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)


def get_container_client() -> ContainerClient:
    """Create and return a ContainerClient instance for the specified container_name."""
    blob_service_client = get_blob_service_client()
    return blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER)


def upload_blob(blob_name: str, file_or_data) -> None:
    """Upload a file or data to Azure Blob Storage as a blob."""
    container_client = get_container_client()
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file_or_data, overwrite=True)


def read_blob(blob_name: str) -> bytes:
    """Download a blob from Azure Blob Storage as a file or data."""
    container_client = get_container_client()
    blob_client = container_client.get_blob_client(blob_name)
    response = blob_client.download_blob()
    data = response.readall()
    return data


def get_blob_json(blob_name: str) -> dict:
    """Download a blob from Azure Blob Storage as a JSON object."""
    return json.loads(read_blob(blob_name))


def get_blob_string(blob_name: str) -> str:
    """Download a blob from Azure Blob Storage as a string."""
    return read_blob(blob_name).decode("utf-8")


def get_blob_image(blob_name: str) -> BytesIO:
    """Download a blob from Azure Blob Storage as an image."""
    return BytesIO(read_blob(blob_name))


def list_blobs(prefix: str = None):
    """List all blobs in a container with an optional prefix."""
    container_client = get_container_client()
    blob_list = container_client.list_blobs(name_starts_with=prefix)
    return blob_list


def delete_blob(blob_name: str) -> None:
    """Delete a blob from Azure Blob Storage."""
    container_client = get_container_client()
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.delete_blob()


def blob_exists(blob_name: str) -> bool:

    
    """Check if a blob exists in the container."""
    try:
        blob_client = get_container_client().get_blob_client(blob_name)
        blob_client.get_blob_properties()
        return True
    except Exception as e:
        print(f"Exception while checking blob existence: {e}")
        return False
    

#********************************************************************************************************************
# Specific functions for azurefed that will utilize the storage basic helper functions
#********************************************************************************************************************

# Create a user folder in the Azure Blob Storage container
def create_user_folder(alias):
    """
    Create a user folder in the Azure Blob Storage container if it does not already exist.

        Args:
        alias (str): The alias of the user.
    """
    init_file_name = f"{alias}/initialize.txt"

    try:
        # Check if the settings file exists, if not use the default settings file and create a new settings file for the user
        if not blob_exists(init_file_name):
            # Write the initialized file to the user folder with current timestamp
            upload_blob(init_file_name, f"Initialized: {datetime.now()}")
    except Exception as e:
        print(f"Failed to load or create user settings: {e}")
        raise
