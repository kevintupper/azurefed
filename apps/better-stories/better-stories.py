# better-stories.py - better-stories app for azurefed.com.

# Standard imports
import asyncio

# Third-party imports
import streamlit as st


# Local imports
from helpers import helper_auth as authentication
from helpers import helper_utils as utils

#***********************************************************************************************
# Menu Definition
#***********************************************************************************************
MENU_ITEMS = [
    {"menu_title": "Better Stories", "return_value": "better_stories", "submenu":[
        {"menu_title": "Better Stories", "return_value": "better_stories"},
        {"menu_title": "Introduction", "return_value": "introduction"},
    ]},
    {"menu_title": "Large Language Models", "return_value": "large_language_models", "submenu":[
        {"menu_title": "What is a GPT?", "return_value": "what_is_gpt"},
        {"menu_title": "Visiting France?", "return_value": "visiting_france"},
    ]},

    {"menu_title": "Powerful Prompts", "return_value": "powerful_prompts", "submenu":[
        {"menu_title": "Demonstration", "return_value": "demonstration"},
        {"menu_title": "Prompting Tips", "return_value": "prompting_tips"},
    ]},

    {"menu_title": "Guidelines and Limitations", "return_value": "guidelines_and_limitations", "submenu":[
        {"menu_title": "Security & Privacy", "return_value": "security_and_privacy"},
        {"menu_title": "Model Variations", "return_value": "model_variations"},
        {"menu_title": "Hallucinations", "return_value": "hallucinations"},
    ]},

]


#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# Better-stories Page
async def better_stories():
    """
    Display the better-stories page.
    """
    utils.display_local_image("./img/better-stories.png")


# Introduction Page
async def introduction():
    """
    Display the introduction page.
    """
    utils.display_local_image("./img/introduction.png")

# What is a GPT? Page
async def what_is_gpt():
    """
    Display the what is a GPT? page.
    """
    utils.display_local_image("./img/what-is-a-gpt.png")

# Visiting France? Page
async def visiting_france():
    """
    Display the visiting France? page.
    """
    utils.display_local_image("./img/visiting-france.png")

# Demonstration Page
async def demonstration():
    """
    Display the demonstration page.
    """
    st.markdown("## Demonstration")
    st.markdown("[Microsoft Copilot](https://copilot.microsoft.com)")

# Prompting Tips
async def prompting_tips():
    """
    Display the better ideas page.
    """
    st.markdown("## Prompting Tips")
    st.markdown("### 1. **Be Specific**: The more specific your prompt, the more specific the output will be.")
    st.markdown("### 2. **Be Clear**: Make sure your prompt is clear and concise.")
    st.markdown("### 3. **Be Creative**: Use your imagination to come up with unique and interesting prompts.")
    st.markdown("### 4. **Be Patient**: Sometimes it takes a few tries to get the desired output.")
    
    
# Security & Privacy Page
async def security_and_privacy():
    """
    Display the security & privacy page.
    """
    utils.display_local_image("./img/security-and-privacy.png")

# Model Variations Page
async def model_variations():
    """
    Display the model variations page.
    """
    st.markdown("## Model Variations")
    st.markdown("### 1. Different models may produce different results for the same prompt.")
    st.markdown("### 2. Some models may be better suited for certain types of prompts.")
    st.markdown("### 3. Experiment with different models to see which one works best for your needs.")
    st.markdown("")
    st.markdown("[Model Catalog](https://ai.azure.com/explore/models)")



# Hallucinations Page
async def hallucinations():
    """
    Display the hallucinations page.
    """
    utils.display_local_image("./img/hallucinations.png")
    st.markdown("[Content Safety](https://contentsafety.cognitive.azure.com/)")



#***********************************************************************************************
# Page display and styling helper functions
#***********************************************************************************************
async def initialize_app_session_state():
    """
    Initialize the session state variables for the application.
    """
    
    # Check if the session state variables are already initialized
    if "app_initialized" not in st.session_state:
        # Initialize the session state variables
        st.session_state.app_initialized = True


async def reset_app_session_state():
    """
    Reset the session state variables for the application.
    """
   
    # Reset the session state variables
    st.session_state.app_initialized = False


async def setup_styling_and_menu():
    """
    Setup the page styling and sidebar options.
    """
    
    # Insert custom CSS into the page
    utils.insert_custom_css('./helpers/style_helpers/site.css')
    utils.insert_custom_css('./helpers/style_helpers/menu.css')

    # Setup the menu
    menu_items = []
    for item in MENU_ITEMS:
        # Filter submenu items if present
        submenu = item.get("submenu", [])
        
        # Add the parent menu item if not in hidden items, with filtered submenu
        item["submenu"] = submenu
        menu_items.append(item)

    # Setup the sidebar menu options
    with st.sidebar:
        with st.container():
            st.markdown("<div class='logo-divider'></div>", unsafe_allow_html=True)

            # Get the selected title from filtered_menu_items
            selected_title = st.radio("Main navigation", [item["menu_title"] for item in menu_items], label_visibility="collapsed")

            st.markdown("<div class='tight-divider'></div>", unsafe_allow_html=True)

            # Get the selected menu item
            selected_menu_item = [item for item in menu_items if item["menu_title"] == selected_title][0]

            # Filter submenu based on selected main navigation and aoai_mode
            submenu_items = selected_menu_item["submenu"]

            # Check if there is a submenu
            if submenu_items:
                # Display the submenu as radio buttons
                selected_submenu_title = st.radio("Sub navigation", [item["menu_title"] for item in submenu_items], label_visibility="collapsed")
                selected_return_value = [item["return_value"] for item in submenu_items if item["menu_title"] == selected_submenu_title][0]
            else:
                selected_return_value = selected_menu_item["return_value"]

    return selected_return_value    


# Display Page Content
async def display_page_content(selected_return_value):
    """
    Display the page content based on the selected menu item.
    """

    # Check if the function exists in the global namespace
    if selected_return_value in globals():
    
        # Call the function based on its name
        await globals()[selected_return_value]()


#***********************************************************************************************
# Main function
#***********************************************************************************************
async def main():
        """
        Main function that runs Streamlit app.
        """
    
        # Configure the Streamlit app settings
        st.set_page_config(
            page_title="Azure Fed Demo Manager",                        # Set the page title
            page_icon="",                                               # Set the page icon
            layout="wide",                                              # Set the page layout to wide
            initial_sidebar_state="expanded",                           # Set the initial state of the sidebar to expanded
        )
    
        # Enforce user authentication by checking to see if the user has signed in 
        authentication.enforce_authentication()
    
        # Check if user_info is available in the session_state (the use has signed in)
        if "user_info" in st.session_state and st.session_state.user_info is not None:
    
            # Initialize the session state vars for the application
            await initialize_app_session_state()

            # Setup the page and get the selected_title
            selected_return_value = await setup_styling_and_menu()
    
            # Display the page content based on the selected menu item
            await display_page_content(selected_return_value)
    
        else:
            # Display the sign in screen
            authentication.display_sign_in_screen()



# Call the main function
if __name__ == "__main__":
    asyncio.run(main())

