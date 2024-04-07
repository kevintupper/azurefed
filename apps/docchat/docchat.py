# docchat.py - docchat app for azurefed.com.

# Standard imports
import asyncio
import base64
from datetime import datetime
import time

# Third-party imports
import streamlit as st

# Local imports
from helpers import helper_auth as authentication
from helpers import helper_utils as utils
from helpers import helper_graphlit 
from helpers import helper_storage as storage

#***********************************************************************************************
# Menu Definition
#***********************************************************************************************
MENU_ITEMS = [
    {"menu_title": "Introduction", "return_value": "introduction", "submenu": []},
    {"menu_title": "Load Files", "return_value": "load_files", "submenu": []},
    {"menu_title": "Doc Chat", "return_value": "docchat", "submenu": []},

    # Add your menu items here
    # {"menu_title": "Demo 2", "return_value": "demo_2", "submenu": [
    #     {"menu_title": "Next 1", "return_value": "demo_2_next_1"},
    #     {"menu_title": "Next 2", "return_value": "demo_2_next_2"},
    # ]},

]


#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# Introduction Page
async def introduction():
    """
    Display the introduction page.
    """

    # Set the page title
    st.markdown("### Introduction")
    st.write("Welcome to Doc Chat. This application allows you to interact with the Graphlit service to experience chat over documents. You can also upload files to Azure Blob Storage for further processing.")
    st.markdown("**Current User Information**")
    st.json(st.session_state.user_info)


# Docchat Page
async def docchat():
    """
    Display the docchat page.
    """

    # Set the page title
    st.markdown("### Doc Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state['graphlit_specification_id'] is None:
        error_message = helper_graphlit.create_specification()

        if error_message is not None:
            st.error(f"Failed to create specification. {error_message}")

    if st.session_state['graphlit_conversation_id'] is None:
        error_message = helper_graphlit.create_conversation()

    if error_message is not None:
        st.error(f"Failed to create conversation. {error_message}")

    try:
        if prompt := st.chat_input("Ask me anything about your content."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response, error_message = helper_graphlit.prompt_conversation(prompt)
                
                if error_message is not None:
                    st.error(f"Failed to prompt conversation. {error_message}")
                else:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
    except:
        st.warning("You need to generate a token before chatting with your file.")



# Load Files Page
async def load_files():
    """
    Display the load files page.
    """

    # Set the page title
    st.markdown("### Load File")
    
    

    # Radio button to show tables of file types supported
    table_to_show = st.radio("Supported file types", ["Documents","Audio","Video","Images","Animations","Data","Emails","Code","Packages","Other"],label_visibility="collapsed", horizontal=True)

    # Placeholder for uploaded_files_status message
    uploaded_files_status = st.empty()


    # Display the supported file types based on the selected table
    file_types = []
    extra_info = None
    if table_to_show == "Documents":
        file_types_table, extra_info = get_file_types_documents()
        file_types = ["pdf","htm","html","mhtml","docx","xlsx","pptx","rtf","md","txt","text","csv","tsv","log"]
    elif table_to_show == "Audio":
        file_types_table, extra_info  = get_file_types_audio()
        file_types = ["wav","m4a","aac","mp4","mpa","m2a","mp3","flac","ogg","opus","aiff","aifc","aif","ac3","wma"]
    elif table_to_show == "Video":
        file_types_table, extra_info  = get_file_types_video()
        file_types = ["mp4","mov","moov","qt"]            
    elif table_to_show == "Images":
        file_types_table, extra_info  = get_file_types_audio()
        file_types = ["jpg","jpeg","jpe","png","heif","heic","webp","bmp","tif","tiff"]
    elif table_to_show == "Animations":
        file_types_table, extra_info  = get_file_types_animations()      
        file_types = ["gif","apng"]      
    elif table_to_show == "Data":
        file_types_table, extra_info  = get_file_types_data()
        file_types = ["json","xml"]
    elif table_to_show == "Emails":
        file_types_table, extra_info  = get_file_types_emails()
        file_types = ["eml","msg"]
    elif table_to_show == "Code":
        file_types_table, extra_info  = get_file_types_code()
        file_types = ["py","js","ts","go","cs","c","cpp","java","php","rb","swift","rs"]
    elif table_to_show == "Packages":
        file_types_table, extra_info  = get_file_types_packages()
        file_types = ["zip"]
    elif table_to_show == "Other":
        file_types_table, extra_info  = get_file_types_other()
        file_types = ["dwf","dwfx","dxf","dwg","svg","geojson","shp","fbx","3ds","dae","gltf","glb","drc","obj","stl","usdz","las","laz","e57","ptx","pts","ply"]
    
    # Create a form for the file uploader    
    with st.form("data_content_form"):    
        if file_types:
            # Display the file uploader
            uploaded_file = st.file_uploader("Upload a file", type=file_types, accept_multiple_files=False, label_visibility="collapsed")

            # Display the supported file types table
            show_file_type_table(file_types_table)
            
            if extra_info:
                st.write("")
                st.info(extra_info)

            submit_content = st.form_submit_button("Submit")

            # Now, handle actions based on submit_data outside the form's scope
            if submit_content and uploaded_file:
                st.session_state.messages = []
                st.session_state['graphlit_content_done'] = False

                
                # Make sure we have a token
                if st.session_state.graphlit_token:      
                     
                    # Clean up previous session state
                    if st.session_state['graphlit_workflow_id'] is None:
                        error_message = helper_graphlit.create_workflow()

                        if error_message is not None:
                            st.error(f"Failed to create workflow. {error_message}")

                    if st.session_state['graphlit_content_id'] is not None:
                        with st.spinner('Deleting existing content... Please wait.'):
                            helper_graphlit.delete_content()
                        st.session_state["graphlit_content_id"] = None

                    start_time = time.time()
                        
                    # Read the file content
                    file_content = uploaded_file.getvalue()
                    
                    base64_content = base64.b64encode(file_content).decode('utf-8')

                    # Display spinner while processing
                    with st.spinner('Ingesting file... Please wait.'):
                        error_message = helper_graphlit.ingest_file(uploaded_file.name, uploaded_file.type, base64_content)

                        if error_message is not None:
                            st.error(f"Failed to ingest file. {error_message}")
                        else:
                            duration = time.time() - start_time

                            current_time = datetime.now()
                            formatted_time = current_time.strftime("%H:%M:%S")

                            st.success(f"File ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

                    # Once done, notify the user
                    st.session_state["graphlit_content_done"] = True

                    placeholder = st.empty()
                else:
                    st.error("Please fill in all the connection information.")
        
    ### KT'S CODE TO UPLOAD FILES TO BLOB    
    # # Display the file uploader
    # uploaded_files = st.file_uploader("Upload a file", type=file_types, accept_multiple_files=True, label_visibility="collapsed", )
    
    # # Display the supported file types table
    # show_file_type_table(file_types_table)
    
    # if extra_info:
    #     st.write("")
    #     st.info(extra_info)

    # # Check if files were uploaded
    # if uploaded_files:

    #     # Create a user folder in Azure Blob Storage if it does not already exist
    #     alias = authentication.get_user_alias(st.session_state.user_info)
    #     storage.create_user_folder(alias)

    #     # Upload the files and show the status
    #     with uploaded_files_status.expander("Uploaded Files", expanded=True):

    #         # Loop through the uploaded files
    #         for file in uploaded_files:

    #             # Blob name is the alias of the user and the name of the file
    #             blob_name = f"{alias}/docchat/files/{file.name}"  
                
    #             # Read the file content
    #             file_content = file.getvalue()
                
    #             # Upload the file content to Azure Blob Storage
    #             storage.upload_blob(blob_name, file_content)
                
    #             # Optionally, you can show a success message for each upload
    #             st.write(f"'{file.name}' uploaded successfully.")



#***********************************************************************************************
# Page display and styling helper functions
#***********************************************************************************************

def show_file_type_table(markdown_table):
    """ 
    Display the markdown table full width.
    """
    
    st.markdown("""
<style>
/* Target all tables within the Streamlit app and set them to full width */
table {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)
    
    # Display the table in Streamlit using Markdown
    st.markdown(markdown_table, unsafe_allow_html=True)

def get_file_types_documents():
    """
    Show the supported file types for documents.
    """
    
    markdown_text = """
| File Type               | File Extension       |
|-------------------------|----------------------|
| PDF                     | .pdf                 |
| HTML                    | .htm .html           |
| MIME Archive            | .mhtml               |
| Word Document           | .docx                |
| Excel Spreadsheet       | .xlsx                |
| PowerPoint Presentation | .pptx                |
| Rich Text Format        | .rtf                 |
| Markdown                | .md                  |
| Text                    | .txt .text           |
| Comma-Separated Values  | .csv                 |
| Tab-Separated Values    | .tsv                 |
| Log File                | .log                 |
"""
    return markdown_text, "PDF files will automatically extract and ingest any embedded images, upon file preparation."
       
def get_file_types_audio():
    """
    Show the supported file types for audio.
    """
    
    markdown_text = """
| File Type             | File Extension        |
|-----------------------|-----------------------|
| WAV                   | .wav                  |
| MPEG-4 Audio          | .m4a .aac .mp4        |
| MPEG Audio            | .mpa .m2a             |
| MP3                   | .mp3                  |
| FLAC                  | .flac                 |
| OGG                   | .ogg .opus            |
| AIFF                  | .aiff .aifc .aif      |
| AC-3                  | .ac3                  |
| Windows Media Audio   | .wma                  |
"""
    return markdown_text, None
    
def get_file_types_video():
    """
    Show the supported file types for video.
    """
    
    markdown_text = """
| File Type        | File Extension   |
|------------------|------------------|
| MPEG-4           | .mp4             |
| QuickTime Video  | .mov .moov .qt   |
"""
    return markdown_text, None        

def get_file_types_images():
    """
    Show the supported file types for images.
    """
    
    markdown_text = """
| File Type        | File Extension      |
|------------------|---------------------|
| JPEG             | .jpg .jpeg .jpe     |
| PNG              | .png                |
| HEIC             | .heif .heic         |
| WebP             | .webp               |
| Windows Bitmap   | .bmp                |
| TIFF             | .tif .tiff          |
"""
    return markdown_text, None
   
def get_file_types_animations():
    """
    Show the supported file types for animations.
    """
    
    markdown_text = """
| File Type     | File Extension |
|---------------|----------------|
| GIF           | .gif           |
| Animated PNG  | .apng          |
""" 
    return markdown_text, None
    
def get_file_types_data():
    """
    Show the supported file types for data.
    """
    
    markdown_text = """
| File Type | File Extension |
|-----------|----------------|
| JSON      | .json          |
| XML       | .xml           |
"""
    return markdown_text, None
     
def get_file_types_emails():
    """
    Show the supported file types for emails.
    """
    
    markdown_text = """
| File Type | File Extension |
|-----------|----------------|
| EML       | .eml           |
| MSG       | .msg           |
"""
    return markdown_text, "Emails will automatically extract and ingest any attached files, upon file preparation."  
    
def get_file_types_code():
    """
    Show the supported file types for code.
    """
    
    markdown_text = """
| File Type   | File Extension |
|-------------|----------------|
| Python      | .py            |
| JavaScript  | .js            |
| TypeScript  | .ts            |
| Go          | .go            |
| C#          | .cs            |
| C           | .c             |
| C++         | .cpp           |
| Java        | .java          |
| PHP         | .php           |
| Ruby        | .rb            |
| Swift       | .swift         |
| Rust        | .rs            |
"""
    return markdown_text, "Graphlit recognized 50+ code file extensions.  If you find a code file extension we don't support, please reach out to us and we will add it."
    
def get_file_types_packages():
    """
    Show the supported file types for packages.
    """
    
    markdown_text = """
| File Type | File Extension |
|-----------|----------------|
| ZIP       | .zip           |
"""
    return markdown_text,"Packages will automatically extract and ingest any packaged files, upon file preparation."
    
def get_file_types_other():
    """
    Show the supported file types for other files.
    """
    
    markdown_text = """
| File Type                   | File Extension        |
|-----------------------------|-----------------------|
| Design Web Format           | .dwf .dwfx            |
| AutoCAD DXF                 | .dxf                  |
| Autodesk Drawing            | .dwg                  |
| SVG                         | .svg                  |
| GeoJSON                     | .geojson              |
| ESRI Shapefile              | .shp                  |
| Autodesk FBX                | .fbx                  |
| 3D Studio                   | .3ds                  |
| Collada                     | .dae                  |
| GL Transmission Format      | .gltf .glb            |
| Google Draco                | .drc                  |
| Wavefront                   | .obj                  |
| 3D Systems CAD              | .stl                  |
| Universal Scene Description | .usdz                 |
| LAS                         | .las .laz             |
| E57                         | .e57                  |
| PTS                         | .ptx .pts             |
| PLY                         | .ply                  |
"""
    return markdown_text, None
    
async def initialize_app_session_state():
    """
    Initialize the session state variables for the application.
    """
    
    # Check if the session state variables are already initialized
    if "app_initialized" not in st.session_state:
        
        # Initialize the graphlit service
        helper_graphlit.initialize_graphlit_service()
        
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

