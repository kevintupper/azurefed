# Utility helper functions for applicaiions using Streamlit

# Import required libraries
import streamlit as st
from PIL import Image
from PIL import UnidentifiedImageError
import os
import json
import logging


# Function to read the contents of a file
@st.cache_resource
def read_file(file_path, safe_mode=False):
    """
    Reads the contents of a file.
    
    Args:
        file_path (str): Path to the file.
        safe_mode (bool): If True, function won't raise an exception on error.

    Returns:
        str or None: The content of the file or None if an error occurs and safe_mode is True.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File '{file_path}' not found.")
    except Exception as e:
        logging.error(f"Error reading file '{file_path}': {e}")
    if safe_mode:
        return None
    raise


# Function to read the contents of a JSON file
def load_json_from_file(file_path):
    file_content = read_file(file_path, safe_mode=True)
    if file_content is not None:
        try:
            return json.loads(file_content)
        except json.JSONDecodeError:
            st.error("Error parsing JSON from the file.")
            st.stop()
    else:
        st.error("File not found or unable to read the file.")
        st.stop()


# Function to get the custom CSS
@st.cache_resource
def get_custom_css(css_file):
    """
    Reads a custom CSS file and wraps its content in HTML style tags.

    Args:
        css_file (str): The path to the CSS file.

    Returns:
        str: The CSS content wrapped in <style> tags.

    Raises:
        Exception: Propagates exceptions from the read_file function.
    """
    try:
        # Read the custom CSS from the file
        custom_css = read_file(css_file)
        logging.info("Custom CSS loaded")

        # Wrap the custom CSS in style tags
        return f"<style>{custom_css}</style>"
    except Exception as e:
        logging.error(f"Error loading CSS file {css_file}: {e}")
        raise


# Function to insert custom CSS
def insert_custom_css(css_file):
    """
    Inserts custom CSS into the Streamlit application.

    Args:
        css_file (str): The path to the CSS file.
    """
    # Insert the custom CSS into the app
    st.markdown(get_custom_css(css_file), unsafe_allow_html=True)