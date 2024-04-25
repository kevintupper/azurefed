# aiea.py - aiea app for azurefed.com.

# Standard imports
import asyncio
import json

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

    {"menu_title": "Content Generation", "return_value": "content_generator", "submenu": [
        {"menu_title": "Outline", "return_value": "outline"},
        {"menu_title": "Guidance", "return_value": "guidance"},
        {"menu_title": "Next 2", "return_value": "demo_2_next_2"},
    ]},

]

OUTLINE_SYSTEM_MESSAGE = """
You are an AI Assistant designed to create structured outlines in JSON format for various types of documents. Your capabilities enable you to tailor each outline according to specific input parameters including topic, content type, target audience, and purpose of the document. Your outputs must align with a predefined schema to maintain consistency and clarity.

**Parameters for Outline Creation:**
- **topic**: The main subject of the document.
- **content_type**: The nature of the document (e.g., report, executive briefing, research paper, LinkedIn post).
- **target_audience**: The intended readership (e.g., students, professionals, government officials).
- **purpose**: The goal or objective of the document (e.g., to inform, to persuade, to update).
- **word_count**: The suggested length of the content.
- **key_ideas_to_include**: List any specific points or themes that must be addressed in the document.

**Fixed Output Schema:**
- Your output should strictly follow this JSON schema:
```json
{
  "document_title": "string",
  "introduction": {
    "section_title": "string",
    "section_content": "string"
  },
  "sections": [
    {
      "section_title": "string",
      "section_content": "string",
      "subsections": [
        {
          "subsection_title": "string",
          "subsection_content": "string"
        }
      ]
    }
  ],
  "conclusion": {
    "section_title": "string",
    "section_content": "string"
  }
}
```

**Flexibility in Structure**: While you must adhere to the section titles as outlined, you are allowed to omit entire sections or subsections if they are not relevant to the specific document you are creating. However, you cannot change the names of these sections.

**Output Requirements:**
- Ensure that each outline is detailed, directly addressing the given parameters, and formatted to facilitate clarity and organization. Your outputs should help users quickly understand the document’s structure and content at a glance.

By following this guidance, your performance will consistently meet user expectations across various document types, ensuring each outline is effective and appropriate to its purpose.
"""


#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# Content Generation - Outline Page
async def outline():
    """
    Page for generating content outlines. The objective is to get user input to fill out the following JSON schema for having AI generate an outline.

        {
            "topic": "<Insert topic here>",
            "content_type": "<Specify type of content, e.g., article, blog post, report>",
            "target_audience": "<Define the target audience, e.g., industry professionals, general public, specific age group>",
            "purpose": "<Describe the purpose of the content, e.g., to inform, persuade, entertain>",
            "words": "<Specify word count range, e.g., 2000-3000>",
            "key_ideas_to_include": [
                "<Idea 1>",
                "<Idea 2>",
                "<Idea 3>"
            ],
            "author_role": "<Describe the role or perspective of the author, e.g., expert, observer, participant>"
        }

    """


    # Set the page title
    st.markdown("### Content Generation - Outline")
    

    # Use a select box to select the chat service
    # The selected value is automatically updated in the session state
    selected_service = st.selectbox("Select chat service", st.session_state.chat_services, key="outline_chat_service", index=0)

    # Get type of content to generate
    # Eventually get this from the content_type.json file for now we will allow defaulted free form text
    content_type = st.text_input("Content type", placeholder="Specify the type of content to generate, e.g., article, blog post, report, briefing, presentation.")
  
    # Topic
    topic = st.text_input("Topic", placeholder="Enter the topic with as much specificity as possible.")

    # Target Audience    
    target_audience = st.text_input("Target Audience", placeholder="Enter the target audience with as much specifity as possible.")

    # Purpose
    purpose = st.text_input("Purpose", placeholder="Enter the purpose of the content, e.g., to inform, persuade, educate.")

    # Words
    words = st.text_input("Words", placeholder="Enter the approximate word count range for the content.")

    # Key Ideas to Include
    key_ideas_to_include = st.text_area("Key Ideas to Include", placeholder="Enter key points or ideas you want included.")

    # Author Role
    author_role = st.text_input("Author Role", placeholder="Describe the role or perspective of the author, e.g., advisor, policy analyst, developer.")

            #     # Tone/Style
            #     default_tone_style = """Maintain a warm and engaging tone that is welcoming yet professional.
            # Address the target audience directly and plainly. Avoid jargon and complex terms to ensure clarity and accessibility.
            # Write at an 8th grade reading level, using straightforward languages.
            # When explaining complex concepts, break them down into bite-sized, easily digestible parts.
            # Assume the reader is intelligent. Use analogies sparingly, only when necessary to clarify particularly challenging ideas.
            # Avoid salesy language and focus on providing value to the reader."""
                    
            #     tone_style = st.text_area("Tone/Style", value=default_tone_style, height=200)


    # Submit button
    submit_button = st.button("Submit")

    if submit_button:
        st.success("Form submitted successfully!")

        response_holder = st.empty()


        # Create the user input content
        user_outline_content_json = {
            "topic": topic,
            "content_type": content_type,
            "target_audience": target_audience,
            "purpose": purpose,
            "words": words,
            "key_ideas_to_include": key_ideas_to_include,
            "author_role": author_role
        }

        # Convert the user input content to a JSON string
        user_outline_content = json.dumps(user_outline_content_json, indent=2)

        # Get and display the response from the chat service
        response = await sk_helper.generate_streaming_response(
            response_holder,
            chat_service=  st.session_state.get(f"{selected_service}_service"),
            system_message=OUTLINE_SYSTEM_MESSAGE,
            chat_history=None,
            user_input=user_outline_content,
            temperature=0.7,
            top_p=1.0,
            stream=True,
            max_tokens=2500
        )
            

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

        # Setup the assistant session state variables
        st.session_state.outline_chat_service = st.session_state.chat_services[0]

        # Initialize the session state variables
        st.session_state.app_initialized = True


async def reset_app_session_state():
    """
    Reset the session state variables for the application.
    """
   
    # Initialize the session state variables
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

