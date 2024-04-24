# aiea.py - aiea app for azurefed.com.

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

    {"menu_title": "Content Generation", "return_value": "content_generator", "submenu": [
        {"menu_title": "Guidance", "return_value": "guidance"},
        {"menu_title": "Next 2", "return_value": "demo_2_next_2"},
    ]},

]


#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# Content Generation - Guidance Page
async def guidance():
    """
    Display the aiea page.
    """

    # Set the page title
    st.markdown("### Content Generation - Guidance")
    
    # Get type of content to generate
    content_type = st.radio("Type", ["Social Post", "Video Talk Track", "LinkedIn Article", "Research Paper"], index=0, horizontal=True)
    
    # Topic
    topic = st.text_area("Topic", placeholder="Enter the topic with as much specificity as possible or instruct agent to refine topic.")

    # Target Audience    
    target_audience = st.text_area("Target Audience", placeholder="Enter the target audience with as much specifity as possible.")

    # Tone/Style
    default_tone_style = """Maintain a warm and engaging tone that is welcoming yet professional.
Address the target audience directly and plainly. Avoid jargon and complex terms to ensure clarity and accessibility.
Write at an 8th grade reading level, using straightforward languages.
When explaining complex concepts, break them down into bite-sized, easily digestible parts.
Assume the reader is intelligent. Use analogies sparingly, only when necessary to clarify particularly challenging ideas.
Avoid salesy language and focus on providing value to the reader."""
        
    tone_style = st.text_area("Tone/Style", value=default_tone_style, height=200)
    
    # Content Length
    content_length = st.text_input("Content Length", placeholder="Enter the approximate length and density of the content.")
    
    # Ideas to Include
    ideas_to_include = st.text_area("Ideas to Include", placeholder="Enter key points or ideas you want included.")
    
    # Resources
    resources = st.text_area("Resources", placeholder="List any specific resources or links to include in the research.")

    # Checkbox for human in the loop
    human_in_the_loop = st.checkbox("Human in the Loop", value=False, help="Check this box if you want a human to review or intervene in the content generation process.")

    # Submit button
    submit_button = st.button("Submit")

    if submit_button:
        st.success("Form submitted successfully!")
        # Here, you would typically handle the form submission logic, such as saving the data or passing it to another function.
        # User guidance



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

