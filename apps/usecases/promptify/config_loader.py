# Description: This module contains the functions to load and validate the package configuration.

# Imports
import pathlib
import os
import yaml
from .helpers import get_package_dir

def resolve_env_variables(config):
    """
    Resolve environment variable references in the config dictionary. Raises an error for unresolved required fields.

    Parameters:
    - config (dict): The dictionary containing the configuration values.

    Returns:
    - dict: The updated config dictionary with resolved environment variable references.
    """
    required_fields = ['azure_endpoint', 'api_key', 'api_version', 'model']
    for key, value in config.items():
        if isinstance(value, str) and value.startswith("$"):
            env_var = value[1:]  # Strip the leading $
            resolved_value = os.getenv(env_var)
            if resolved_value is None and key in required_fields:
                raise EnvironmentError(f"Required environment variable {env_var} for config field '{key}' is not set.")
            elif resolved_value is None:
                print(f"Warning: Environment variable {env_var} for config field '{key}' is not set. Proceeding with defaults or leaving unset.")
            else:
                config[key] = resolved_value
    return config


def validate_config(config):
    """
    Validate the configuration dictionary after environment variables have been resolved.

    Parameters:
    - config (dict): The configuration dictionary to be validated.

    Raises:
    - ValueError: If any of the required fields are missing in the configuration.

    Returns:
    - None
    """
    required_fields = ['azure_endpoint', 'api_key', 'api_version', 'model']
    missing_fields = [field for field in required_fields if field not in config or not config[field]]
    if missing_fields:
        raise ValueError(f"Missing or unresolved required configuration fields: {', '.join(missing_fields)}")

    

def load_config(package_name):
    """
    Load the package configuration from the package_config.yml file.

    Args:
        package_name (str): The name of the package.

    Returns:
        dict: The loaded package configuration.

    Raises:
        FileNotFoundError: If the package configuration file is not found.
    """
    package_path = get_package_dir(package_name)

    config_file = pathlib.Path(package_path) / 'prompt_config.yml'

    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Resolve any environment variable references
    config = resolve_env_variables(config)

    # Validate the resolved configuration
    validate_config(config)

    return config