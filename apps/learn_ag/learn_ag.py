# learn_ag.py - learn_ag app for azurefed.com.

# Standard imports
import asyncio

# Third-party imports
import streamlit as st


# Local imports
from helpers import helper_auth as authentication
from helpers import helper_utils as utils
from helpers import helper_autogen as ag

from autogen import ConversableAgent

#***********************************************************************************************
# Menu Definition
#***********************************************************************************************
MENU_ITEMS = [
    {"menu_title": "Learn_ag", "return_value": "learn_ag", "submenu": []},

    # Add your menu items here
    # {"menu_title": "Demo 2", "return_value": "demo_2", "submenu": [
    #     {"menu_title": "Next 1", "return_value": "demo_2_next_1"},
    #     {"menu_title": "Next 2", "return_value": "demo_2_next_2"},
    # ]},

]


#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# Learn_ag Page
async def learn_ag():
    """
    Display the learn_ag page.
    """

    # Set the page title
    st.markdown("### Learn_ag App - Azure Fed Demo Environment")
    
    if st.button("Tell me a joke"):
        
        abbot = ConversableAgent(
            "Abbot",
            system_message="Your name is Abbot and you are the straight man comedic duo.",
            llm_config=ag.DEFAULT_LLM_CONFIG,
            human_input_mode="NEVER",  # Never ask for human input.
        )

        costello = ConversableAgent(
            "Costello",
            system_message="Your name is Costello and you are the stooge part of a duo of comedians.",
            llm_config=ag.DEFAULT_LLM_CONFIG,
            human_input_mode="NEVER",  # Never ask for human input.
        )
        
        result = abbot.initiate_chat(costello, message="Costello, I own a baseball team.", max_turns=3)
        
        st.write(result)


#        agent = ag.get_conversable_agent()
#        reply = agent.generate_reply(messages=[{"content": "Tell me a joke.", "role": "user"}])
#        st.markdown(reply)



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

