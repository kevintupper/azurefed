# sk.py - sk app for azurefed.com.

# Standard imports
import asyncio

# Third-party imports
import streamlit as st


# Local imports
from helpers import helper_auth as authentication
from helpers import helper_utils as utils
from helpers import helper_sk as sk


#***********************************************************************************************
# Menu Definition
#***********************************************************************************************
MENU_ITEMS = [
    {"menu_title": "Chat", "return_value": "chat", "submenu": []},
    {"menu_title": " Reframe input", "return_value": "reframe_input", "submenu": []},
    {"menu_title": " Validate domain", "return_value": "validate_domain", "submenu": []},
    {"menu_title": " Need filings", "return_value": "need_filings", "submenu": []},
    {"menu_title": " Symbols", "return_value": "symbols", "submenu": []},
    {"menu_title": " Filing Type", "return_value": "filing_type", "submenu": []},
    {"menu_title": " Filing Period", "return_value": "filing_period", "submenu": []},
]


#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# Chat Page
async def chat():
    """
    Display the chat page.
    """

    # Function to display message history
    def display_message_history(container, chat_history, selected_service_id):
        """
        Display the message history.
        """
        if container != None and chat_history != None:
            container.markdown(f"**{selected_service_id}**")
            for message in chat_history.messages:
                with container.chat_message(message.role):
                    st.markdown(message.content)


    # Build the chat page
     
    # Set the page title
    st.markdown("### Chat")


    # Initialize vars to hold placeholder and response for chat service
    response_1 = None
    response_2 = None
    response_coro_1 = None
    response_coro_2 = None
    
    
    # Sidebar options to select the chat services to use
    selected_chat_service = await display_sidebar_chat_services()


    # Initialize col1 and col2 for single or dual services
    col1, col2 = st.columns(2) if selected_chat_service == "both" else (st, None)


    # Initialize the selected service for one or both 
    selected_service_id_1 = "gpt_35_turbo" if selected_chat_service == "both" else selected_chat_service
    selected_service_id_2 = "gpt_4" if selected_chat_service == "both" else None
    
    
    # Get the chat service
    curent_chat_service_1 = st.session_state.get(f"{selected_service_id_1}_service")
    curent_chat_service_2 = st.session_state.get(f"{selected_service_id_2}_service") if selected_chat_service == "both" else None
    
    # Get the chat history
    current_chat_history_1 = st.session_state.get(f"{selected_service_id_1}_history")
    current_chat_history_2 = st.session_state.get(f"{selected_service_id_2}_history") if selected_chat_service == "both" else None


    # Display the chat history for the first service and the second service if available
    display_message_history(col1, current_chat_history_1, selected_service_id_1)
    display_message_history(col2, current_chat_history_2, selected_service_id_2) 


    # Get the user input
    if prompt := st.chat_input():
        
        # Add the user input to the chat history and display the user input
        current_chat_history_1.add_user_message(prompt)
        if col2:
            current_chat_history_2.add_user_message(prompt)
        
        # Display the user input
        with col1.chat_message("user"):
            st.markdown(prompt)
        if col2:
            with col2.chat_message("user"):
                st.markdown(prompt)

        # Create placeholders for the assistant's response and setup the routine to get the responses
        with col1.chat_message("assistant"):
            placeholder_1 = st.empty()
            
            # Initialize the response coroutine
            response_coro_1 = sk.generate_streaming_response(
                response_holder=placeholder_1,
                chat_service=curent_chat_service_1,
                system_message="You are a helpful AI assistant.",
                chat_history=current_chat_history_1,
                user_input=None, # Already added to chat history.
            )

        if col2:
            with col2:
                # Placeholder for the assistant's response
                with st.chat_message("assistant"):
                    placeholder_2 = st.empty()

                # Initialize the response coroutine
                response_coro_2 = sk.generate_streaming_response(
                    response_holder=placeholder_2,
                    chat_service=curent_chat_service_2,
                    system_message="You are a helpful AI assistant.",
                    chat_history=current_chat_history_2,
                    user_input=None, # Already added to chat history.
                )
                
        # Build the response coroutines
        coroutines = [response_coro_1]
        if col2: 
            coroutines.append(response_coro_2)

        # Get the responses
        responses = await asyncio.gather(*coroutines)

        # Now, assign responses conditionally
        response_1 = responses[0]
        if len(responses) > 1:
            response_2 = responses[1]
            

        # Add the assistant's response to the chat history
        current_chat_history_1.add_assistant_message(response_1)
        if selected_chat_service == "both":
            current_chat_history_2.add_assistant_message(response_2)


        # Important: Update the session state with the modified chat history
        st.session_state[f"{selected_service_id_1}_history"] = current_chat_history_1
        if selected_chat_service == "both":
            st.session_state[f"{selected_service_id_2}_history"] = current_chat_history_2 


# Validate Domain Page
async def reframe_input():
    """
    Display the remframe input page.
    """
    
    # Build the reframe input
    st.markdown("### 1. Reframe Input")


    # Get the system message
    st.markdown("**System Message**")
    default_system_message = "IINSTRUCTIONS: Review the supplied sequence of user input messages and reframe the last one so that it can stand alone and be sent to an AI assistant."
    system_message = st.text_area("Enter the system message", value=default_system_message, height=300, label_visibility="collapsed")
    
    # Get the user input
    st.markdown("### 2. User Input")
    default_user_input = """Sequence of user input messages:
- Graph the earnings of AAPL stock over the past 5 years.
- Include Microsoft too
"""
    user_input = st.text_area("Enter the system message", value=default_user_input, height=100, label_visibility="collapsed")

    # Sidebar options to select the chat services to use
    selected_chat_service = await display_sidebar_chat_services()

    # Initialize the selected service for one or both 
    selected_service_id_1 = "gpt_35_turbo" if selected_chat_service == "both" else selected_chat_service
    selected_service_id_2 = "gpt_4" if selected_chat_service == "both" else None

    # Initialize the chat function
    current_chat_function_1 = st.session_state.get(f"{selected_service_id_1}_function")
    current_chat_function_2 = st.session_state.get(f"{selected_service_id_2}_function") if selected_chat_service == "both" else None

    if st.button("Reframe Input"):
        # Placeholder for the reframed input
        holder = st.empty()
        
        # response = await sk.generate_response(
        #     response_holder=holder,
        #     chat_function=current_chat_function_1,
        #     system_message=system_message,
        #     chat_history=None,
        #     user_input=user_input,
        #     temperature=0.0,
        #     top_p=0.1,
        #     max_tokens=5,
        # )




#***********************************************************************************************
# Page display and styling helper functions
#***********************************************************************************************
async def display_sidebar_chat_services():
    """
    Display the sidebar options to select the chat services.
    """
    
    # Services to allow for this demo
    available_chat_services = ["gpt_35_turbo","gpt_4","both"]
    
    # Setup the sidebar options
    with st.sidebar:
        
        # Display and return the chat service to use
        st.markdown("**Chat Service**")
        selected_service = st.radio("Select chat service",
                                    options=available_chat_services,
                                    index=0,
                                    label_visibility="collapsed")

        # Button to clear chat history
        st.markdown("**Commands**")
        if st.sidebar.button("Clear chat history"):
            await reset_app_session_state()    
    
    # Return the selected chat service
    return selected_service


async def initialize_app_session_state():
    """
    Initialize the session state variables for the application.
    """
    
    # Initialize chat_sevices if necssary
    if "chat_services" not in st.session_state:
        sk.initialize_chat_services()
        

    # Initialize chat app specific settings
    if "chat_app_initialized" not in st.session_state:
        
        # Create a chat_history for each service
        for service_name in st.session_state.chat_services:
            st.session_state[f"{service_name}_history"] = sk.new_chat_history()

        # Flag as initialized.
        st.session_state.chat_app_initialized = True


async def reset_app_session_state():
    """
    Reset some of the session state variables for the application.
    """
    
    # Reset the chat service histories
    for service_name in st.session_state.chat_services:
        st.session_state[f"{service_name}_history"] = sk.new_chat_history()
    

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

