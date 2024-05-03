import zipfile
import os
import yaml
import openai
import streamlit as st

def clean_environment():
    """Remove sensitive OpenAI API information from environment variables."""
    keys_to_remove = ["OPENAI_API_KEY", "OPENAI_ORGANIZATION_ID", "OPENAI_DEFAULT_ORGANIZATION_ID"]
    for key in keys_to_remove:
        os.environ.pop(key, None)

def upload_to_openai(file):
    """Upload a file to OpenAI and return its file ID or None if the upload fails."""
    try:
        with open(file.name, "rb") as f:
            response = openai.File.create(file=f, purpose="assistants")
        return response['id']
    except Exception as e:
        st.error(f"Failed to upload file to OpenAI: {e}")
        return None

def export_assistant(assistant_name, assistant_model, assistant_prompt, files_uploaded):
    """Export assistant configuration and files to a ZIP file and return its binary content."""
    config_file_name = "config_assistant.yaml"
    prompt_file_name = "prompt.txt"
    zip_file_name = "config_assistant.zip"

    with open(config_file_name, "w") as file_yaml:
        yaml.dump({"name": assistant_name, "model": assistant_model}, file_yaml)

    with open(prompt_file_name, "w") as file_prompt:
        file_prompt.write(assistant_prompt)

    with zipfile.ZipFile(zip_file_name, "w") as zip_file:
        zip_file.write(config_file_name)
        zip_file.write(prompt_file_name)
        if files_uploaded:
            for file in files_uploaded:
                zip_file.write(file.name)

    return open(zip_file_name, "rb")

def create_assistant_from_config_file(file_up, client):
    """Create an assistant from a configuration file, uploading any additional files included."""
    temp_folder = "temp_folder"
    config_zip_file = "config_assistant.zip"

    try:
        # Save the uploaded config file and extract its contents
        with open(config_zip_file, "wb") as f:
            f.write(file_up.getbuffer())

        with zipfile.ZipFile(config_zip_file, "r") as zip_ref:
            zip_ref.extractall(temp_folder)

        # Load assistant configuration from YAML
        with open(os.path.join(temp_folder, "config_assistant.yaml")) as yaml_file:
            config_data = yaml.safe_load(yaml_file)
        assistant_name = config_data.get('name', '')
        assistant_model = config_data.get('model', '')

        # Display assistant info
        st.write(f"Assistant Name: {assistant_name}")
        st.write(f"Assistant Model: {assistant_model}")

        # Load the assistant prompt
        with open(os.path.join(temp_folder, "prompt.txt")) as prompt_file:
            assistant_prompt = prompt_file.read()

        stored_file_ids = []
        # Upload any additional files found in the temp folder
        for item in os.listdir(temp_folder):
            file_path = os.path.join(temp_folder, item)
            if os.path.isfile(file_path) and item not in ["config_assistant.yaml", "prompt.txt"]:
                file_id = upload_to_openai(open(file_path, "rb"))
                if file_id:
                    stored_file_ids.append(file_id)

        # Create the assistant
        my_assistant = client.create_assistant(
            instructions=assistant_prompt,
            name=assistant_name,
            model=assistant_model,
            file_ids=stored_file_ids,
        )

        return my_assistant
    finally:
        # Clean up temporary files and folder
        if os.path.exists(temp_folder):
            for item in os.listdir(temp_folder):
                os.remove(os.path.join(temp_folder, item))
            os.rmdir(temp_folder)
