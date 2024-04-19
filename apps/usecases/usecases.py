# usecases.py - usecases app for azurefed.com.

# Standard imports
import asyncio

# Third-party imports
import streamlit as st


# Local imports
from helpers import helper_auth as authentication
from helpers import helper_utils as utils
from helpers import helper_phidata as helper_phidata

#***********************************************************************************************
# Menu Definition
#***********************************************************************************************
MENU_ITEMS = [
    {"menu_title": "Innovate with AI", "return_value": "", "submenu": [
        {"menu_title": "Innovate 1", "return_value": "innovate_1"},
        {"menu_title": "Innovate 2", "return_value": "innovate_2"},
        {"menu_title": "Innovate 3", "return_value": "innovate_3"},
    ]},

    {"menu_title": "Grant Auditor Assistant", "return_value": "", "submenu": [
        {"menu_title": "GAA - Vignette - 1", "return_value": "gaa_vignette_1"},
        {"menu_title": "GAA - Vignette - 2", "return_value": "gaa_vignette_2"},
        {"menu_title": "GAA - Vignette - 3", "return_value": "gaa_vignette_3"},
    ]},

    {"menu_title": "Rulemaking Assistant", "return_value": "", "submenu": [
        {"menu_title": "RA - Vignette - 1", "return_value": "ra_vignette_1"},
        {"menu_title": "RA - Vignette - 2", "return_value": "ra_vignette_2"},
        {"menu_title": "RA - Vignette - 3", "return_value": "ra_vignette_3"},
    ]},

    {"menu_title": "Productivity Assistant", "return_value": "", "submenu": [
        {"menu_title": "PA - Vignette - 1", "return_value": "pa_vignette_1"},
        {"menu_title": "PA - Vignette - 2", "return_value": "pa_vignette_2"},
        {"menu_title": "PA - Vignette - 3", "return_value": "pa_vignette_3"},
    ]},
]


#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# Innovate 1
async def innovate_1():
    # Set the page title
    st.markdown("### Innovate 1")
    st.markdown("This is the Innovate 1 page.")

    # Get a prompt from the user
    prompt = st.text_input("Enter a prompt", "What is the capital of France?")

    # Get an assistant.
    assistant = helper_phidata.get_assistant()

    # Run the assistant
    if st.button("Run Assistant"):
        assistant.print_response(prompt)

# Innovate 2
async def innovate_2():
    # Set the page title
    st.markdown("### Innovate 2")
    st.markdown("This is the Innovate 2 page.")

# Innovate 1
async def innovate_3():
    # Set the page title
    st.markdown("### Innovate 3")
    st.markdown("This is the Innovate 3 page.")

# GAA Vignette 1
async def gaa_vignette_1():
    # Set the page title
    st.markdown("### GAA Vignette 1")
    st.markdown("This is the GAA Vignette 1 page.")

# GAA Vignette 2
async def gaa_vignette_2():
    # Set the page title
    st.markdown("### GAA Vignette 2")
    st.markdown("This is the GAA Vignette 2 page.")

# GAA Vignette 3
async def gaa_vignette_3():
    # Set the page title
    st.markdown("### GAA Vignette 3")
    st.markdown("This is the GAA Vignette 3 page.")

# RA Vignette 1
async def ra_vignette_1():
    # Set the page title
    st.markdown("### RA Vignette 1")
    st.markdown("This is the RA Vignette 1 page.")

# RA Vignette 2
async def ra_vignette_2():
    # Set the page title
    st.markdown("### RA Vignette 2")
    st.markdown("This is the RA Vignette 2 page.")

# RA Vignette 3
async def ra_vignette_3():
    # Set the page title
    st.markdown("### RA Vignette 3")
    st.markdown("This is the RA Vignette 3 page.")

# PA Vignette 1
async def pa_vignette_1():
    # Set the page title
    st.markdown("### PA Vignette 1")
    st.markdown("This is the PA Vignette 1 page.")

# PA Vignette 2
async def pa_vignette_2():
    # Set the page title
    st.markdown("### PA Vignette 2")
    st.markdown("This is the PA Vignette 2 page.")
    

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

