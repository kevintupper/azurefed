# Imports
import os
import time
from dotenv import load_dotenv
import streamlit as st
from openai import AzureOpenAI

# Initialization function
def init():
    """Initializes the application by loading environment variables and setting up the Azure OpenAI client."""
    # Load environment variables
    load_dotenv()

    # Setup Azure OpenAI client and initialize session state variables
    if "aoai_client" not in st.session_state:
        st.session_state.aoai_client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )

    # Initialize session state variables for message history, run status, file IDs, and thread ID
    for var in ["messages", "run", "file_ids", "thread_id"]:
        if var not in st.session_state:
            st.session_state[var] = [] if var == "file_ids" else None

# Main function
def main():
    """Defines the main flow of the application, allowing users to create, update, or test an AI assistant."""
    # Configure the Streamlit app settings
    st.set_page_config(
        page_title="AI Assistant Configurator",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Display app title and description
    st.markdown("## AI Assistant Configurator")
    st.caption('Azure OpenAI GPT-4 offers guidable AI assistants to help you with tasks.')

    # User option selection for assistant configuration
    create_or_import = st.radio(
        label="Modality",
        options=["Create a new assistant", "Update an existing assistant", "Test an assistant"],
        index=0,  # Default to creating a new assistant
        horizontal=True,
        label_visibility="collapsed"  # Hide the label to integrate it as part of the markdown text above
    )

    # Handle user selection for creating a new assistant
    if create_or_import == "Create a new assistant":
        create_new_assistant()  

    # Handle user selection for updating an assistant
    elif create_or_import == "Update an existing assistant":
        update_existing_assistant()  
        
    # Handle user selection for testing an assistant
    elif create_or_import == "Test an assistant":
        test_assistant()  


def create_new_assistant():
    """Handles the creation of a new AI assistant, including name definition, prompt setting, and file uploads."""

    # Get the assistant's name
    st.markdown("#### Assistant Name")
    assistant_name = st.text_input("Assistant Name", "", help="Enter the name of the assistant")

    # Proceed if an assistant name has been entered
    if assistant_name:

        # Define the assistant's prompt
        st.markdown("#### Assistant Definition")
        assistant_prompt = st.text_area("Assistant Prompt", "", help="Enter the assistant prompt", height=300)

        # Option to upload files
        upload_files = st.checkbox("Upload files to supply the assistant with knowledge?", value=False)
        if upload_files:
            # File uploader
            file_up = st.file_uploader("Upload File", type=['.c', '.cpp', '.ipynb', '.docx', '.html', '.java', '.json', '.md', '.pdf', '.php', '.pptx', '.py', '.rb', '.tex', '.txt'], accept_multiple_files=True)
            if file_up:
                # Placeholder for the file upload logic
                # In the actual implementation, you would upload these files and store their IDs in session_state.file_ids
                st.session_state.file_ids = ["mock_file_id"] * len(file_up)

        if st.button("Build Assistant") and assistant_prompt:

            # Create the assistant
            with st.spinner("Assistant creation in progress..."):

                if "file_ids" in st.session_state and st.session_state.file_ids:
                    # Create the assistant with file uploads
                    st.success("Assistant created successfully with File and Retrieval")
                else:
                    # Create the assistant without file uploads
                    assistant = st.session_state.aoai_client.beta.assistants.create(
                        instructions = assistant_prompt,
                        model = os.getenv("AZURE_OPENAI_API_DEPLOYMENT"),
                        tools=[{"type": "code_interpreter"}]
                    )     
                    st.success("✅Assistant created successfully")

                # Provide options to use or share the assistant
                st.success("✅Assistant created successfully")
                st.info(f"ID of the assistant: {assistant.assistant_id}")
                st.error("⛔ Remember to save the ID of the assistant to use it later")
                
                col_a, col_b = st.columns(2)
                col_a.info("📥 To use the assistant, copy the ID and paste it in the 'Use an Assistant' section")
                col_b.info("📥 To share the assistant, download Assistant Configuration File and send it")



def create_new_assistant():
    """Handles the creation of a new AI assistant, including name definition, prompt setting, and file uploads."""

    # Get the assistant's name
    st.markdown("#### Assistant Name")
    assistant_name = st.text_input("Assistant Name", "", help="Enter the name of the assistant", label_visibility="collapsed")

    # Proceed if an assistant name has been entered
    if assistant_name:
        st.markdown("#### Assistant Definition")

        # Define the assistant prompt
        assistant_prompt = st.text_area("Assistant Prompt", "", help="Enter the assistant prompt", height=300, label_visibility="collapsed")

        # Option to upload files
        upload_files = st.checkbox("Upload files to supply the assistant with knowledge?", value=False)

        if upload_files:
            # File uploader
            file_up = st.file_uploader("Upload File", type=['.c', '.cpp', '.ipynb', '.docx', '.html', '.java', '.json', '.md', '.pdf', '.php', '.pptx', '.py', '.rb', '.tex', '.txt'], accept_multiple_files=True)
            
            if file_up:
                # Check if the number of files exceeds the limit
                if len(file_up) > 20:
                    st.error("You can upload a maximum of 20 files.")
                else:
                    # This is a placeholder for the actual file upload logic
                    st.info("Remember to click on the 'Upload File' button to upload the files.")
                    if st.button("Upload File"):
                        # Placeholder for the upload process
                        st.write(f"Uploading {len(file_up)} files...")
                        # Example of handling uploaded files - actual implementation would involve uploading to Azure/OpenAI
                        for uploaded_file in file_up:
                            # For demonstration purposes, we're just showing file names
                            st.write(f"Uploaded {uploaded_file.name}")
                        # Update the session state with file IDs after upload (mock implementation)
                        st.session_state.file_ids = [f"{file.name}_id" for file in file_up]

        if st.button("Build Assistant") and assistant_prompt:
            # Placeholder for creating the assistant with Azure OpenAI
            st.success(f"Assistant '{assistant_name}' created successfully.")
            # Mock assistant ID generation
            assistant_id = "mock_assistant_id"
            st.info(f"ID of the assistant: {assistant_id}")
            st.session_state.assistant_id = assistant_id  # Saving the assistant ID in session state

# Note: Actual implementation details for interacting with Azure OpenAI would depend on their API and SDK


def update_existing_assistant():
    """Allows users to update an existing AI assistant."""
    st.markdown("#### Update an Existing Assistant")
    
    # Placeholder for selecting an assistant to update
    # This could be a dropdown populated with existing assistants' names or IDs
    assistant_id = st.selectbox("Select an Assistant to Update", ["Assistant 1", "Assistant 2"], index=0)

    # Once an assistant is selected, provide options for updating its details
    new_name = st.text_input("New Name", help="Enter a new name for the assistant")
    new_prompt = st.text_area("New Prompt", help="Enter a new prompt for the assistant", height=300)

    # Option to update files - Simplified version without actual upload logic
    update_files = st.checkbox("Update files for the assistant?", value=False)
    if update_files:
        st.file_uploader("Upload New Files", accept_multiple_files=True)

    if st.button("Update Assistant"):
        # Placeholder for the assistant update logic
        st.success(f"Assistant '{assistant_id}' updated successfully.")
        # Implement the actual update logic here, possibly interacting with the Azure OpenAI API


def test_assistant():
    """Allows users to test an AI assistant by sending prompts and displaying responses."""
    st.markdown("#### Test an Assistant")
    
    # Placeholder for selecting an assistant to test
    assistant_id = st.selectbox("Select an Assistant to Test", ["Assistant 1", "Assistant 2"], index=0)
    test_prompt = st.text_area("Test Prompt", help="Enter a prompt to test the assistant", height=150)

    if st.button("Test Assistant"):
        # Placeholder for sending the test prompt to the assistant and retrieving the response
        # The actual implementation would interact with the Azure OpenAI API
        mock_response = "This is a mock response based on the test prompt."
        st.text_area("Assistant Response", value=mock_response, height=150, help="The assistant's response to the test prompt", readonly=True)



if __name__ == '__main__':
    init()
    main()
    print(st.session_state.file_ids)  # For debugging purposes, printing the file IDs stored in the session
