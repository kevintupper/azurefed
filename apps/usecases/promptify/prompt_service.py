# This is the main file for executing the prompts. It is the entry point for promptify.

# Imports from the Python standard library
import json
import os
from openai import AzureOpenAI

# Imports from the promptify package
from .config_loader import load_config
from .template_processor import process_template
from .helpers import get_package_dir


# Functions
def print_configuration(config):
    """
    Print the configuration details in a readable format.

    Parameters:
    - config (dict): Configuration dictionary loaded from prompt_config.yml.

    """
    print("Configuration Details:")
    print(json.dumps(config, indent=4))


def setup_message_text(prompt_folder, system_message_replacements, user_message_replacements):
    """
    Load the system and user message templates, process them with the replacements, and return the processed messages.
    """

    # Get the path to the prompt folder
    prompt_folder_path = get_package_dir(prompt_folder)

    # Load the system and user message templates and process them with the replacements
    system_template_path = prompt_folder_path / 'system_message.txt'
    system_message = process_template(system_template_path, system_message_replacements)
    user_template_path = prompt_folder_path / 'user_message.txt'
    user_message = process_template(user_template_path, user_message_replacements)

    # Create the message text
    message_text = [
        {"role":"system", "content": system_message},
        {"role":"user", "content": user_message},
    ]

    # Return the message text
    return message_text


def get_response(prompt_folder, system_message_replacements, user_message_replacements):
    """
    Load the configuration, process the system and user messages with replacements, 
    and print the configuration and processed messages.

    Parameters:
    - prompt_folder (str): The folder name where the prompt configuration and templates are located.
    - system_message_replacements (list of str): Replacements for the system message template.
    - user_message_replacements (list of str): Replacements for the user message template.

    """

    # Load the configuration, system message, and user message (use template_processor for replacements)
    config = load_config(prompt_folder)
    message_text = setup_message_text(prompt_folder, system_message_replacements, user_message_replacements)


    # Setup AOAI client
    aoai_client = AzureOpenAI(
        azure_endpoint = config['azure_endpoint'],
        api_key= config['api_key'],  
        api_version= config['api_version']
    )

    # Get the response from AOAI
    completion = aoai_client.chat.completions.create(
        model = config['model'],
        messages = message_text,
        temperature = config.get('temperature', 0.7),
        max_tokens = config.get('max_tokens', 250),
        top_p =  config.get('top_p', 1.0),
        frequency_penalty = config.get('frequency_penalty', 0.0),
        presence_penalty = config['presence_penalty'],
        stop = config.get('stop', None),
        stream = config.get('stream', False)
    )
    # Return the completion object.  (Note: when streaming we don't get all the meta.  When not streaming we get the full object returned.)
    return completion

