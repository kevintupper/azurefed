# main.py - main app for azurefed.com website

# Standard imports
import asyncio

# Third-party imports
import streamlit as st

# SK imports
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.contents.chat_history import ChatHistory

# Local imports
from helpers import helper_auth as authentication
from helpers import helper_utils as utils
from helpers import helper_sk as sk_helper

#***********************************************************************************************
# Menu Definition
#***********************************************************************************************
MENU_ITEMS = [
    {"menu_title": "AOAI", "return_value": "aoai", "submenu": []},
    {"menu_title": "Chat", "return_value": "chat", "submenu": []},
    {"menu_title": "Compare", "return_value": "chat_compare", "submenu": []},
]


#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# AOAI Page
async def aoai():
    """
    Display the chat page.
    """

    # Set the page title
    st.markdown("### AOAI")

    # Define page content.
    st.json(st.session_state.user_info)


# Chat Page
async def chat():
    """
    Display the chat page.
    """

    # Set the page title
    st.markdown("### Semantic Kernel Chat")
    
    # Setup the sidebar to choose the chat service
    with st.sidebar:
        with st.container():
            st.markdown("**Chat Service**")
            
            # Use a select box to select the chat service
            # The selected value is automatically updated in the session state
            selected_service = st.selectbox("Select chat service",
                                            st.session_state.chat_services,
                                            key="active_chat_service",
                                            index=0,
                                            label_visibility="collapsed")
            # # Create the radio button to select the chat service
            # # The selected value is automatically updated in the session state
            # selected_service = st.radio("Select chat service",
            #                             st.session_state.chat_services,
            #                             key="active_chat_service",
            #                             index=0,
            #                             label_visibility="collapsed")


    # Display the active service outside the sidebar for confirmation
    st.write(f"Active chat service: {st.session_state.active_chat_service}")

    # Show the current chat history for the active service and set local variables
    selected_service_id = st.session_state.active_chat_service
    current_chat_history = st.session_state[f"{selected_service_id}_history"]
    current_chat_function = st.session_state[f"{selected_service_id}_function"]


    # Show the current chat history
    for message in current_chat_history.messages:
        with st.chat_message(message.role):
            st.markdown(message.content)

    # Get the user input
    if prompt := st.chat_input():
        # Add the user input to the chat history and display the user input
        current_chat_history.add_user_message(prompt)
        
        # Display the user input
        with st.chat_message("user"):
            st.markdown(prompt)

        # Placeholder for the assistant's response
        with st.chat_message("assistant"):
            response_holder = st.empty()

            # Get and display the response from the chat service
            response = await sk_helper.generate_response(
                response_holder,
                current_chat_function,
                current_chat_history,
                prompt)

            # Add the assistant's response to the chat history
            current_chat_history.add_assistant_message(response)

            # Important: Update the session state with the modified chat history
            st.session_state[f"{selected_service_id}_history"] = current_chat_history


async def chat_compare():
    """
    Display the chat page.
    """

    # Set the page title
    st.markdown("### Chat Model Comparison")
    
    # Initialize the chat history and function for each chat service
    current_chat_history_1 = None
    current_chat_history_2 = None
    current_chat_function_1 = None
    current_chat_function_2 = None
    selected_service_id_1 = None
    selected_service_id_2 = None
    placeholder_1 = None
    placeholder_2 = None
    response_1 = None
    response_2 = None

    # Display the chat services side by side
    col1, col2 = st.columns(2)
    
    with col1:
        selected_service_1 = st.selectbox("Select chat service",
                                          st.session_state.chat_services,
                                          key="active_chat_service_1",
                                          index=0,
                                          label_visibility="collapsed")
        
        # Show the current chat history for the active service and set local variables
        selected_service_id_1 = selected_service_1
        current_chat_history_1 = st.session_state[f"{selected_service_id_1}_history"]
        current_chat_function_1 = st.session_state[f"{selected_service_id_1}_function"]

        # Show the current chat history
        for message in current_chat_history_1.messages:
            with st.chat_message(message.role):
                st.markdown(message.content)

    with col2:
        selected_service_2 = st.selectbox("Select chat service",
                                          st.session_state.chat_services,
                                          key="active_chat_service_2",
                                          index=1,
                                          label_visibility="collapsed")

        # Show the current chat history for the active service and set local variables
        selected_service_id_2 = selected_service_2
        current_chat_history_2 = st.session_state[f"{selected_service_id_2}_history"]
        current_chat_function_2 = st.session_state[f"{selected_service_id_2}_function"]

        # Show the current chat history
        for message in current_chat_history_2.messages:
            with st.chat_message(message.role):
                st.markdown(message.content)

        
    # Get the user input
    if prompt := st.chat_input():
        
        # Add the user input to the chat history and display the user input
        current_chat_history_1.add_user_message(prompt)
        current_chat_history_2.add_user_message(prompt)
        

        # Display the user input
        with col1:
            with st.chat_message("user"):
                st.markdown(prompt)
        with col2:
            with st.chat_message("user"):
                st.markdown(prompt)


        # Create placeholders for the assistant's response
        with col1:
            # Placeholder for the assistant's response
            with st.chat_message("assistant"):
                placeholder_1 = st.empty()

                response_coro_1 = sk_helper.generate_response(
                    placeholder_1,
                    current_chat_function_1,
                    current_chat_history_1,
                    prompt)

        with col2:
            # Placeholder for the assistant's response
            with st.chat_message("assistant"):
                placeholder_2 = st.empty()

                response_coro_2 = sk_helper.generate_response(
                    placeholder_2,
                    current_chat_function_2,
                    current_chat_history_2,
                    prompt)

            # Run the coroutines concurrently and wait for all to finish
            response_1, response_2 = await asyncio.gather(response_coro_1, response_coro_2)


            # Add the assistant's response to the chat history
            current_chat_history_1.add_assistant_message(response_1)
            current_chat_history_2.add_assistant_message(response_2)

            # Important: Update the session state with the modified chat history
            st.session_state[f"{selected_service_id_1}_history"] = current_chat_history_1
            st.session_state[f"{selected_service_id_2}_history"] = current_chat_history_2



#***********************************************************************************************
# Page display and styling helper functions
#***********************************************************************************************




async def initialize_app_session_state():
    """
    Initialize the session state variables for the application.
    """
    
    # Check if the session state variables are already initialized
    if "app_initialized" not in st.session_state:
        
        # Initialize the chat services
        sk_helper.initialize_chat_services()
        
        # Initialize the session state variables
        st.session_state.app_initialized = True


async def reset_app_session_state():
    """
    Reset the session state variables for the application.
    """
   
    # Reset the session state variables
    st.session_state.app_initialized = False


def setup_styling_and_menu():
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

#
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
            page_title="AOAI",                                       # Set the page title
            page_icon="",                                               # Set the page icon
            layout="wide",                                              # Set the page layout to wide
            initial_sidebar_state="expanded",                           # Set the initial state of the sidebar to expanded
        )
    
        # Enforce user authentication by checking to see if the user has signed in 
        authentication.enforce_authentication()
    
        # Check if user_info is available in the session_state (the use has signed in)
        if "user_info" in st.session_state and st.session_state.user_info is not None:
    
            # Initialize the app session state
            await initialize_app_session_state()
    
            # Setup the page and get the selected_title
            selected_return_value = setup_styling_and_menu()
    
            # Display the page content based on the selected menu item
            await display_page_content(selected_return_value)
    
        else:
            # Display the sign in screen
            authentication.display_sign_in_screen()



# Call the main function
if __name__ == "__main__":
    asyncio.run(main())