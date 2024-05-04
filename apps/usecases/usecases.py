# usecases.py - usecases app for azurefed.com.

# Standard imports
import asyncio
import json
import requests
import pandas as pd
import time

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
    { "menu_title": "Introduction", "return_value": "introduction", "submenu": [] },
    { "menu_title": "Advanced AI", "return_value": "", "submenu": [
        {"menu_title": "3 Waves of AI", "return_value": "three_waves_of_ai"},
        {"menu_title": "Traditional AI", "return_value": "traditional_ai"},
        {"menu_title": "Generative AI", "return_value": "generative_ai"},
    ]},

    {"menu_title": "Applied AI", "return_value": "", "submenu": [
        {"menu_title": "Capabilities", "return_value": "capabilities"},
        {"menu_title": "Use Cases", "return_value": "use_cases"},
    ]},

    {"menu_title": "Agentic Patterns", "return_value": "", "submenu": [
        {"menu_title": "Non-agentic Workflow", "return_value": "non_agentic_workflow"},
        {"menu_title": "Agentic Workflow", "return_value": "agentic_workflow"},
        {"menu_title": "Reflection", "return_value": "reflection"},
        {"menu_title": "Tool Use", "return_value": "tool_use"},
        {"menu_title": "Planning", "return_value": "planning"},
        {"menu_title": "Multiagent Collaboration", "return_value": "multiagent_collaboration"},
    ]},


    {"menu_title": "Rulemaking Assistant", "return_value": "rulemaking", "submenu": [] },

    {"menu_title": "Content Analyst", "return_value": "", "submenu": [
        {"menu_title": "PA - Vignette - 1", "return_value": "pa_vignette_1"},
        {"menu_title": "PA - Vignette - 2", "return_value": "pa_vignette_2"},
        {"menu_title": "PA - Vignette - 3", "return_value": "pa_vignette_3"},
    ]},


    {"menu_title": "Premonition", "return_value": "", "submenu": [
        {"menu_title": "PA - Vignette - 1", "return_value": "pa_vignette_1"},
        {"menu_title": "PA - Vignette - 2", "return_value": "pa_vignette_2"},
        {"menu_title": "PA - Vignette - 3", "return_value": "pa_vignette_3"},
    ]},
]


#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# Rulemaking Assistant
async def rulemaking():

    # Set the page title and description
    st.markdown("### Stakeholder Analyst Assistant")
    st.markdown("Analyze a proposed rule from regulations.gov for stakeholder concerns and objections.")

    # Display the input fields for the user to enter the docket ID
    docket_id = st.text_input('Docket ID')

    # Initialize the analysis_running flag
    analysis_running = False
    
    # Check if the user has clicked the "Conduct Analysis" button
    if st.button('Conduct Analysis'):

        if docket_id:

            # Set status to "Analyzing the proposed rule..."
            status = st.status("Analyzing the proposed rule...")

            # Display rule and analysis results
            tabRule, tabAnalysis, tabSuggestions = st.tabs(["Proposed Rule", "Stakeholder Analysis", "Overall Suggestions"])

            # Fetch the docket details from the API 
            status.write(f"Fetching {docket_id} from regulations.gov...")
            docket_content = get_docket_details(docket_id)

            # Display and analyze the docket content if available
            if docket_content:
                with tabRule:
                    st.html(docket_content)

                with tabAnalysis:
                    status.write(f"Reviewing rule and determining stakeholders...")




                    st.write("Stakeholder Analysis Results")


                # Simulate analysis running
                i = 1
                while i <= 6:
                    # Your analysis code here...
                    time.sleep(2)  # Simulating analysis process
                    i += 1
                    status.update(label=f"Analyzing rule for stakeholder: {i} ...", state="running")


                with tabSuggestions:
                    st.write("Overall Suggestions") 
                    status.update(label=f"Analysis complete.", state="complete")
    
    # agency_options = load_agencies()

    # selected_agency = st.selectbox('Select Agency', options=list(agency_options.keys()))

    # agency_id = agency_options[selected_agency]
    # docket_id = st.text_input('Docket ID (optional)')
    # keyword = st.text_input('Keyword (optional)')
    # date_posted = st.date_input('Posted Since', value=pd.to_datetime('today'))

    # if st.button('Search'):
    #     results = fetch_rules(agency_id=agency_id, docket_id=docket_id, keyword=keyword, date_posted=date_posted.strftime('%Y-%m-%d'))
    #     if not results.empty:
    #         st.data_editor(results)
    #         st.dataframe(results)
    #     else:
    #         st.write("No results found.") 
    


#***********************************************************************************************
# Page display and styling helper functions
#***********************************************************************************************
# Load agency data from JSON file
@st.cache_data
def load_agencies():
    """Load agency data from a JSON file and return a dictionary of agency names and IDs."""
    with open('./data/reg_dot_gov_particpants.json', 'r') as file:
        agencies = json.load(file)
    return {agency['agency']: agency['agency_id'] for agency in agencies}


def fetch_rules(agency_id, docket_id, keyword, date_posted):
    """Fetch proposed rules from the API based on the provided filters."""
    url = "https://api.regulations.gov/v4/documents"
    params = {
        "api_key": helper_phidata.REGULATIONS_GOV_API_KEY,
        "filter[agencyId]": agency_id,
        "filter[postedDate][ge]": date_posted,      # Date posted filter correctly formatted
        "filter[documentType]": "Proposed Rule",    # Only fetch proposed rules
        "sort": "-postedDate"                       # Sort by posted date in descending order
    }

    # Add optional filters
    if docket_id:
        params["filter[docketId]"] = docket_id
    if keyword:
        params["filter[searchTerm]"] = keyword

    # For debugging: Print the full URL and parameters
    print("Making API Call to:", url)
    print("With parameters:", params)


    response = requests.get(url, params=params)
    if response.status_code == 200:
        json_data = response.json()

        # Select only the relevant fields from the response
        if 'data' in json_data:
            df = pd.json_normalize(json_data['data'])
            df = df.rename(columns={
                'attributes.postedDate': 'Posted Date',
                'attributes.title': 'Title',
                'id': 'Document ID',
                'attributes.commentStartDate': 'Comments Start',
                'attributes.commentEndDate': 'Comments End'
            })
            df['Posted Date'] = pd.to_datetime(df['Posted Date']).dt.strftime('%Y-%m-%d')
            df['Comments Start'] = pd.to_datetime(df['Comments Start']).dt.strftime('%Y-%m-%d')
            df['Comments End'] = pd.to_datetime(df['Comments End']).dt.strftime('%Y-%m-%d')

            # Add a checkbox column for user selection
            df.insert(0, 'Select', False)
            return df
        #['Select','Posted Date', 'Title', 'Document ID', 'Comments Start', 'Comments End']

    else:
        return pd.DataFrame()
    

def get_docket_details(docketId):
    """
    Given a specific docucmentId (docketId) this retrieves the docket content.
    Parameters:
        docketId (str): The document ID of the docket to retrieve.
    """
    
    url = f"https://api.regulations.gov/v4/documents/{docketId}"
    params = {
        "api_key": "4p2Hpwlq1SJ5kOhayfhqeI0D1RtDOo70d8azejwL"
    }
    # For debugging: Print the full URL and parameters
    print("Making API Call to:", url)
    print("With parameters:", params)

    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("API Call Successful!")
        
    # Load the JSON data from the API response
    data = response.json()
    
    # Navigate through the JSON structure to find the file URL for the HTML format
    file_formats = data['data']['attributes']['fileFormats']
    html_url = None
    for file_format in file_formats:
        if file_format['format'] == 'htm':
            html_url = file_format['fileUrl']
            break
    
    # Check if an HTML URL was found
    if not html_url:
        return "No HTML document found in the response."

    # Download the content of the HTML document
    response = requests.get(html_url)
    if response.status_code == 200:
        return response.text
    else:
        print (f"Failed to download the document. Status code: {response.status_code}")
        return None
    

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

