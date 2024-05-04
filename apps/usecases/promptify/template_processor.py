# This script handles processing the template files and replacing the placeholders with the provided replacements.

# Import the required modules
import os
import re
from pathlib import Path


def load_template_file(template_path):
    """
    Load the content of a template file.

    Parameters:
    - template_path (Path): The pathlib.Path object pointing to the template file.

    Returns:
    - str: The content of the template file.

    Raises:
    - FileNotFoundError: If the template file does not exist.
    """
    if not template_path.is_file():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()


def find_highest_placeholder(template_content):
    """
    Find the highest placeholder number in the template content.

    Parameters:
    - template_content (str): The content of the template.

    Returns:
    - int: The highest placeholder number found, or 0 if none found.
    """
    placeholders = re.findall(r'\{(\d+)\}', template_content)
    if not placeholders:
        return 0
    return max(map(int, placeholders))



def replace_placeholders(template_content, replacements):
    """
    Replace placeholder tokens in the template content with the provided replacements.

    Parameters:
    - template_content (str): The content of the template.
    - replacements (list): A list of strings to replace the placeholder tokens.

    Returns:
    - str: The processed template content with placeholders replaced.

    Raises:
    - ValueError: If the number of replacements does not match the number of placeholders.
    """
    highest_placeholder = find_highest_placeholder(template_content)

    if highest_placeholder != len(replacements):
        raise ValueError(f"The number of replacements provided ({len(replacements)}) does not match the highest placeholder number ({highest_placeholder}) in the template.")
    
    for i, replacement in enumerate(replacements, start=1):
        template_content = re.sub(fr'\{{{i}\}}', replacement, template_content)
    
    return template_content


def process_template(template_path, replacements):
    """
    Load, validate, and process a template file with the provided replacements.

    Parameters:
    - template_path (Path): The pathlib.Path object pointing to the template file.
    - replacements (list): A list of strings to replace the placeholder tokens in the template.

    Returns:
    - str: The processed template content.

    Raises:
    - FileNotFoundError: If the template file does not exist.
    - ValueError: If the number of replacements does not match the number of placeholders.
    """
    # Load the template file
    template_content = load_template_file(template_path)
    
    # Replace placeholders with replacements
    return replace_placeholders(template_content, replacements)
