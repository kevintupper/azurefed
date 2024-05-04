# Helper functions for promptify

# Imports
import os
import pathlib

def get_base_dir():
    """
    Fetches the PROMPTIFY_BASE_DIR environment variable.

    Returns:
        str: The value of the PROMPTIFY_BASE_DIR environment variable.

    Raises:
        EnvironmentError: If the PROMPTIFY_BASE_DIR environment variable is not set.
    """    
    base_dir = os.getenv('PROMPTIFY_BASE_DIR')
    if base_dir is None:
        raise EnvironmentError("PROMPTIFY_BASE_DIR environment variable is not set.")
    return base_dir

def get_package_dir(folder_name):
    """
    Fetches the package directory.

    Returns:
        str: The package directory path.
    """    

    package_path = pathlib.Path(get_base_dir()) / folder_name

    if not os.path.isdir(package_path):
        raise FileNotFoundError(f"Package path not found: {package_path}")

    return package_path