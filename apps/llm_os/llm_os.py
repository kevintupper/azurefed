# llm_os.py - llm_os app for azurefed.com.

# Standard imports
import asyncio

# Third-party imports
import streamlit as st

# SK imports
import semantic_kernel as sk

# Local imports
from helpers import helper_auth as authentication
from helpers import helper_utils as utils
from helpers import helper_sk as sk_helper 


#***********************************************************************************************
# Menu Definition
#***********************************************************************************************
MENU_ITEMS = [
    {"menu_title": "Llm_os", "return_value": "llm_os", "submenu": []},

    # Add your menu items here
    {"menu_title": "Demo 2", "return_value": "demo_2", "submenu": [
        {"menu_title": "Next 1", "return_value": "demo_2_next_1"},
        {"menu_title": "Next 2", "return_value": "demo_2_next_2"},
    ]},
]

#***********************************************************************************************
# Sidebar widgets
#***********************************************************************************************

# Allow the user to select the model to use
def model_selection():
    """
    Display the model selection widget.
    """

    # Choose the model to use from the services available in the session state
    selected_service_id = st.sidebar.selectbox("Model to use", st.session_state.chat_services, index=st.session_state.active_chat_service_index)

    # If the selected service is different from the active chat service, update the active chat service, and rerun the app
    if selected_service_id != st.session_state.chat_services[st.session_state.active_chat_service_index]:

        # Set the active chat service index to the index of the selected service
        st.session_state.active_chat_service_index = st.session_state.chat_services.index(selected_service_id)
        st.rerun()
    
    # Return the selected service ID
    return selected_service_id



#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# Llm_os Page
async def llm_os():
    """
    Display the llm_os page.
    """

    # Get the various options from the sidebar

    # Model selection
    selected_service_id = model_selection()




    # Set the page title
    st.markdown("### LLM OS App - Azure Fed Demo Environment")
    st.markdown("**Current User Information**")
    st.json(st.session_state.user_info)

    from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import PromptExecutionSettings

    # Test sk functions
    if st.button("Test SK"):
    
        # Get the kernel
        kernel: sk.Kernel
        kernel = st.session_state.kernel

        fun_plugin = kernel.add_plugin(parent_directory="./sk_plugins/", plugin_name="FunPlugin")
        from semantic_kernel.functions import KernelArguments
        joke_function = fun_plugin["Joke"]

        # Random temp between 0.1 and 1.0
        import random
        temp = 0.1 + (1.0 - 0.1) * random.random()
        settings = PromptExecutionSettings(service_id=selected_service_id, max_tokens=500, temperature=temp, top_p=1.0)
        st.write(f"Temperature: {temp}, model: {selected_service_id}")
        print(settings)
        joke = await kernel.invoke(joke_function, KernelArguments(settings=settings, input="coffee for the sleeping", style="deadpan"))
        st.write(joke)



#***********************************************************************************************
# Page display and styling helper functions
#***********************************************************************************************
async def initialize_app_session_state():
    """
    Initialize the session state variables for the application.
    """

    # Initialize chat_sevices if necssary
    if "chat_services" not in st.session_state:
        print("Initializing chat services")
        sk_helper.initialize_chat_services()

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


# Setup Styling and Menu
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
            # Add logo to the sidebar
            st.logo(image="https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE1Mu3b?ver=5c31")
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
            page_title="LLM OS",                                        # Set the page title
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

