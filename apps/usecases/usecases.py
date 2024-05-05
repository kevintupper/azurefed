# usecases.py - usecases app for azurefed.com.

# Standard imports
import asyncio
import json
import requests
import pandas as pd
import time
import re

# Third-party imports
import streamlit as st


# Local imports
from helpers import helper_auth as authentication
from helpers import helper_utils as utils
from helpers import helper_phidata as helper_phidata
from promptify.prompt_service import get_response

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


    {"menu_title": "Regulatory Insight Analyst", "return_value": "", "submenu": [
        {"menu_title": "Analyst", "return_value": "regulatory_insight_analyst"},
        {"menu_title": "Docket Finder", "return_value": "docket_finder"},
    ]},

]


#***********************************************************************************************
# Page Functions
#***********************************************************************************************

# Regulatroy Insight Analyst
async def regulatory_insight_analyst():

    # Set the page title and description
    st.markdown("### Regulatory Insight Analyst")

    with st.expander("What is the Regulatory Insight Analyst?", expanded=False):
        st.write("The Regulatory Insight Analyst demonstrates the potential of AI in regulatory analysis. Upon entering a Docket ID, this proof of concept dynamically constructs an analysis framework based on the content of the proposed regulation. It utilizes virtual AI experts, who access specialized tools and APIs like eCFR and advanced search functionalities, to thoroughly analyze the rule. The process culminates in a detailed report filled with actionable insights and tailored recommendations, designed to illustrate the dynamic and adaptive capabilities of AI in supporting governmental decision-making.")

    # Display the input fields for the user to enter the Docket ID
    docket_id = st.text_input('Docket ID', placeholder='Enter the Docket ID of the rule you wish to analyze')


    # Check if the user has clicked the "Conduct Analysis" button
    if st.button('Conduct Analysis'):

        if docket_id:

            # Set status label
            status = st.status(label="Conducting analsysis.", state="running")

            # Display rule and analysis results
            tabRule, tabInitialReview, tabOutline, tabNotesForExperts, tabExpertQs, tabExpertAs, tabFirstDraft, tabFinalAnalysis = st.tabs(["Proposed Rule", "Initial Review", "Analysis Outline", "Notes for Experts", "Expert Q's", "Expert A's", "First Draft", "Final Analysis"])

            # Fetch the docket details from the API 
            status.update(label="Fetching proposed rule from regulations.gov.", state="running")
            docket_content = get_docket_details(docket_id)
            docket_content_summary = extract_summary(docket_content)

            # Analyze the docket content
            if docket_content:

                #***********************************************************************************************
                # Write out the rule.
                with tabRule:
                    st.html(docket_content)

                    # Update status log
                    status.write(f"Successfully retrieveed {docket_id} from regulations.gov and posted to 'Proposed Rule' tab.")


                #***********************************************************************************************
                # Initial review of the proposed rule
                status.update(label=f"AI Analyst is conducting an initial review of {docket_id}.", state="running")
                with tabInitialReview:

                    # Call the AI agent to draft the outline
                    response = get_response("initial_review", [], [docket_content])
                    initial_reivew_str = clean_json_from_markdown(response.choices[0].message.content)
                    initial_review = json.loads(initial_reivew_str)

                    # Create a placeholder for the object in case we update it throughout the process
                    initial_review_placeholder = st.empty()
                    initial_review_placeholder.json(initial_review)

                    # Update status log
                    status.write(f"AI Analyst conduted an initial review of the proposed rule and posted the results to the 'Initial Review' tab.")


                #***********************************************************************************************
                # Outline of the analysis
                status.update(label=f"AI Analyst is drafting an outline for the analysis of {docket_id}.", state="running")
                with tabOutline:

                    # Call the AI agent to draft the outline
                    response = get_response("outliner", [], [docket_content, initial_reivew_str])
                    analysis_outline_json_str = clean_json_from_markdown(response.choices[0].message.content)
                    analysis_outline = json.loads(analysis_outline_json_str)

                    # Create a placeholder for the outline since we will be updating it throughout the process
                    analysis_outline_placeholder = st.empty()
                    analysis_outline_placeholder.json(analysis_outline)

                    # Update status log
                    status.write(f"AI Analyst drafted the outline and posted it on 'Analysis Outline' tab.")


                #***********************************************************************************************
                # Generate notes for experts to conduct analysis
                status.update(label=f"AI Analyst is generating notes for experts to conduct analysis of {docket_id}.", state="running")
                with tabNotesForExperts:

                    # Create a placeholder for the analysis outline with research since we will be updating it throughout the process
                    notes_for_experts_placeholder = st.empty()
                    notes_for_experts_placeholder.json(analysis_outline)
                    
                    # Have a researcher generate notes for the experts in the form of Q&A pairs.
                    # We add these notes to the analysis_outline object for the experts to reference.
                    for section in analysis_outline['sections']:
                        for expert in section['consult_experts']:

                            status.update(label=f"AI Analyst is generating notes for the {expert['expert_type']} expert to conduct analysis of {docket_id}.", state="running")
                            
                            response = get_response("expert_notes_from_rule", 
                                                    [docket_content],
                                                    [expert['expert_type'], expert['specialized_knowledge'], expert['reason_for_request'], section['title'],  section['description']])
                            response_str = response.choices[0].message.content
                            response_json_str = clean_json_from_markdown(response_str)
                            data = json.loads(response_json_str)
                            expert['notes_from_rule'] = data
                            
                            # Show intermediate results in the UI
                            notes_for_experts_placeholder.json(analysis_outline)

                    # Update status log
                    status.write(f"AI Analyst added notes for experts to conduct analysis of {docket_id} and posted the resuts on the 'Notes for Experts' tab.")


                #***********************************************************************************************
                # Let the experts define a list of questions to answer for their research
                status.update(label=f"AI Experts are planning their research.", state="running")
                with tabExpertQs:

                    # Create a placeholder for the research since we will be updating it throughout the process
                    expert_qs_placeholder = st.empty()
                    expert_qs_placeholder.json(analysis_outline)
                    
                    # Convert current version of analysis outline (with all the notes) to JSON string for promptify
                    current_outline_and_notes = json.dumps(analysis_outline)

                    # Iterate through the sections and experts in the official analysis_outline to get questions to research
                    for section in analysis_outline['sections']:
                        for expert in section['consult_experts']:

                            status.update(label=f"AI {expert['expert_type']} expert is planning their research.", state="running")

                            # Generate the questions the expert wants answered as a result of their research
                            response = get_response("expert_questions_to_research", 
                                                    [expert['expert_type'], expert['specialized_knowledge']],
                                                    [docket_content, current_outline_and_notes, expert['expert_type'], expert['specialized_knowledge'], section['title'], section['description']])
                            response_str = response.choices[0].message.content
                            response_json_str = clean_json_from_markdown(response_str)
                            data = json.loads(response_json_str)
                            expert['questions_to_research'] = data
                            
                            # Show intermediate results in the UI
                            expert_qs_placeholder.json(analysis_outline)
  
                    # Update status log
                    status.write(f"AI Experts generated the questions they want answered as a result of their research. Results have been posted to the 'Expert Q's' tab.")


                #***********************************************************************************************
                # Let the experts answer the questions 
                # Note: Here we could actually do SERP research or link to other APIs for researching the answers. 
                #       For now we'll rely on the LLM to generate the answers. This risks hallucinating the answers, but it's a demo.
                status.update(label=f"AI Experts are researching the questions and providing responses.", state="running")
                with tabExpertAs:

                    # Create a placeholder for the research since we will be updating it throughout the process
                    expert_as_placeholder = st.empty()
                    expert_as_placeholder.json(analysis_outline)

                    # Iterate through the sections and experts and questions in the official analysis_outline and generate research (answers)
                    for section in analysis_outline['sections']:
                        for expert in section['consult_experts']:

                            # Check if there are questions to research for the expert
                            if "questions_to_research" in expert:
                                # Iterate over each question to research
                                for question_reason_pair in expert['questions_to_research']:

                                    status.update(label=f"AI {expert['expert_type']} expert is researching the questions and providing responses.", state="running")

                                    response = get_response("expert_answers", 
                                                            [expert['expert_type'], expert['specialized_knowledge'],section['description']],
                                                            [docket_content, question_reason_pair['question'], question_reason_pair['reason']])

                                    response_str = response.choices[0].message.content
                                    question_reason_pair['answer'] = response_str
                            
                                    # Show intermediate results in the UI
                                    expert_as_placeholder.json(analysis_outline)
  
                    # Update status log
                    status.write(f"AI Experts have researched and answered their questions. Results have been posted to the 'Expert A's' tab.")


                #***********************************************************************************************
                # Write the first draft
                status.update(label=f"AI Analyst is writing the first draft for each section based on expert research.", state="running")
                with tabFirstDraft:

                    # Create a placeholder for the research since we will be updating it throughout the process
                    first_draft_placeholder = st.empty()
                    first_draft_placeholder.json(analysis_outline)
                    
                    # Iterate through the sections to write teh draft.
                    # Note: This takes the original analysis outline JSON string as input.
                    #       This is to maintain the structure without all of the expert notes for every expert in every section.
                    #       The only section in full sent to the prompt is the one being written.
                    for section in analysis_outline['sections']:
                            
                        status.update(label=f"AI Analyst is writing section '{section['Title']}' based on expert research.", state="running")

                        # Convert section to JSON string for promptify
                        section_json_str = json.dumps(section)

                        # Generate the first draft for the section
                        response = get_response("draft_writer", 
                                                [],
                                                [docket_content, analysis_outline_json_str, section['title'],  section['description'], section_json_str])
                                        
                        response_str = response.choices[0].message.content
                        section['first_draft'] = response_str
                        
                        # Show intermediate results in the UI
                        first_draft_placeholder.json(analysis_outline)
  
                    # Update status log
                    status.write(f"AI Analyst has written the first draft for each section. Results have been posted to the 'First Draft' tab.")

                # Write to disk in case we need to reference it later
                with open(f"./data/first_draft_{docket_id}.json", "w") as file:
                    json.dump(analysis_outline, file)


                #***********************************************************************************************
                # Write the final analysis based on the outline
                # Note: For now we are jus outputing the first draft for each section as the final analysis.
                #       A real implementation would review, edit, and refine the first draft.
                status.update(label=f"Writing the final analysis based on the first draft analysis of {docket_id}.", state="running")
                with tabFinalAnalysis:
                    final_anlysis = create_markdown_draft(analysis_outline)
                    st.markdown(final_anlysis)

                    # Update status log
                    status.write(f"Final analysis written and posted on the 'Final Analysis' tab.")

                # Update the status, we are done.
                status.update(label=f"Analysis complete. The report is posted on the 'Final Analysis' tab", state="complete")



### FUTURE STUFF AND ALSO DOCKET FINDER
                # Modify the analysis outline to inlude placeholders for expert search terms.
#                add_search_terms_to_outline(docket_content_summary, analysis_outline)

                # Rewrite the analysis outline with expert search terms
#                outline_placeholder.json(analysis_outline)



                #     # Call get_response with the docket content to get the subject matter expert prompt
                #     status.update(label="Reviewing rule to determine agent expertise needed . . .", state="running")
                #     output = get_response("sme_prompt", [], [docket_content])
                #     data = json.loads(output.choices[0].message.content.strip('`json \n'))
                #     rule_topic = data['rule_topic']
                #     status.markdown("**Stakeholder Agent Subject Matter Expertise**")
                #     status.write(f"{rule_topic}")

                #     # Now get the list of stakeholders
                #     status.update(label="Getting stakeholders who may be interested in this rule . . .", state="running")
                #     output = get_response("get_stakeholders_prompt", [rule_topic,docket_content], [])
                #     data = json.loads(output.choices[0].message.content.strip('`json \n'))
                #     status.markdown("**Stakeholders**")
                #     stakeholders = data['potential_stakeholders']
                #     for stakeholder in stakeholders:
                #         status.markdown(f"- **{stakeholder['stakeholder']}**: {stakeholder['reason']}")

                #     # Begin drafting the analysis
                #     tabAnalysis.markdown("## Draft Stakeholder Analysis for Docket ID: " + docket_id)  
                #     tabAnalysis.markdown("Prepared by the Stakeholder Agent (an AI) on: " + time.strftime("%Y-%m-%d @ %H:%M"))
                     
                #     tabAnalysis.markdown(f"### Introduction")
                #     tabAnalysis.markdown(f"**Purpose**: The purpose of this analysis is to identify and address the concerns and objections of stakeholders who may be impacted by the proposed rule with docket ID: {docket_id}.")

                #     # Now iterate over each stakeholder and analyze their concerns
                #     tabAnalysis.markdown(f"### Stakeholder Analysis")
                #     for stakeholder in stakeholders:
                #         status.update(label=f"Analyzing rule for stakeholder: {stakeholder['stakeholder']} ...", state="running")
                        
                #         tabAnalysis.markdown(f"#### {stakeholder['stakeholder']}")
                #         tabAnalysis.markdown(f"**Interest**: {stakeholder['reason']}")

                #         output = get_response("stakeholder_analysis_prompt", [stakeholder['stakeholder'],docket_content], [stakeholder['stakeholder'],stakeholder['reason']])
                #         data = json.loads(output.choices[0].message.content.strip('`json \n'))
                #         tabAnalysis.markdown(f"**Likely opinion**: {data['likely_opinion']}")
                #         tabAnalysis.markdown(f"**Concerns or Objections**: {data['concerns_or_objections']}")    
                #         tabAnalysis.markdown(f"**Potential Rule Improvements**: {data['improvements']}")                    

                # with tabSuggestions:
                #     st.write("Overall Suggestions") 
                #     status.update(label=f"Analysis complete.", state="complete")
    
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
    

def add_expert_notes_from_rule_to_outline(docket_content, analysis_outline):
    for section in analysis_outline['sections']:
        for expert in section['consult_experts']:

            response = get_response("expert_notes_from_rule", 
                                    [docket_content],
                                    [expert['expert_type'], expert['specialized_knowledge'], expert['reason_for_request'], section['title'],  section['description']])
            response_str = response.choices[0].message.content
            response_json_str = clean_json_from_markdown(response_str)
            data = json.loads(response_json_str)
            expert['notes_from_rule'] = data

            # Break out of the routine and return after the first expert for demonstration purposes
            # return


def add_expert_questions_to_research_to_outline(docket_content, analysis_outline):

    # Convert analysis outline to JSON string for promptify
    analysis_outline_json_str = json.dumps(analysis_outline)

    # Iterate through the sections and experts to get questions to research
    for section in analysis_outline['sections']:
        for expert in section['consult_experts']:

            response = get_response("expert_questions_to_research", 
                                    [expert['expert_type'], expert['specialized_knowledge']],
                                    [docket_content, analysis_outline_json_str, expert['expert_type'], expert['specialized_knowledge'], section['title'], section['description']])
            response_str = response.choices[0].message.content
            response_json_str = clean_json_from_markdown(response_str)
            data = json.loads(response_json_str)
            expert['questions_to_research'] = data

            # Break out of the routine and return after the first expert for demonstration purposes
            # return


def add_expert_answers_to_questions_to_outline(docket_content, analysis_outline):

    # Iterate through the sections and experts to get questions to research
    for section in analysis_outline['sections']:
        for expert in section['consult_experts']:

            # Check if there are questions to research for the expert
            if "questions_to_research" in expert:
                # Iterate over each question to research
                for question_reason_pair in expert['questions_to_research']:

                    response = get_response("expert_answers", 
                                            [expert['expert_type'], expert['specialized_knowledge'],section['description']],
                                            [docket_content, question_reason_pair['question'], question_reason_pair['reason']])

                    response_str = response.choices[0].message.content
                    question_reason_pair['answer'] = response_str

                # Break out of the routine and return after the first set of questions for demonstration purposes
                # return


def write_draft_for_section(docket_content, analysis_outline, analysis_outline_json_str):

    # Note: this takes the original analysis outline JSON string as input to maintain the structure without all of the expert notes for every expert

    for section in analysis_outline['sections']:
            
            # Convert section to JSON string for promptify
            section_json_str = json.dumps(section)

            response = get_response("draft_writer", 
                                    [],
                                    [docket_content, analysis_outline_json_str, section['title'],  section['description'], section_json_str])
                            
            response_str = response.choices[0].message.content
            section['first_draft'] = response_str


def generate_expert_search_terms(docket_summary, section_title, section_description, expert_type, specialized_knowledge, reason_for_request):
    # Placeholder for the real function that generates search terms based on expert's details
    # Here you'd replace this logic with your black box function.
    return ["geopolitics", "international relations", "security alliances"]


def add_search_terms_to_outline(docket_content_summary, analysis_outline):
    for section in analysis_outline['sections']:
        for expert in section['consult_experts']:
            # Generate and insert search terms for each expert
            expert['search_terms'] = generate_expert_search_terms(docket_content_summary, section['title'], section['description'], expert['expert_type'], expert['specialized_knowledge'], expert['reason_for_request'])


def process_document(document):
    analysis_title = document['analysis_title']
    print(f"Processing document: {analysis_title}\n")
    
    for section in document['sections']:
        title = section['title']
        description = section['description']
        consult_experts = section['consult_experts']
        
        # Printing extracted data for demonstration
        print(f"Section Title: {title}")
        print(f"Description: {description}")
        
        if consult_experts:
            print("Experts to Consult:")
            for expert in consult_experts:
                expert_type = expert['expert_type']
                specialized_knowledge = expert['specialized_knowledge']
                reason_for_request = expert['reason_for_request']
                print(f"  - Expert Type: {expert_type}")
                print(f"    Specialized Knowledge: {specialized_knowledge}")
                print(f"    Reason for Request: {reason_for_request}")
        else:
            print("No experts to consult.")
        
        print("\n")  # Newline for better readability between sections
    
        # Here you can add further processing logic for each section
        # For example, generating a report, sending data to another function, etc.



def create_markdown_draft(data):

    # Initialize the markdown output    
    markdown_output = f"## {data['analysis_title']}\n\n"
    
    for section in data['sections']:
        # Generate the header for the section
        markdown_output += f"### {section['title']}\n"
        
        # Insert the first draft for the content
        markdown_output += f"{section['first_draft']}" + "\n\n"
        
    return markdown_output


def clean_json_from_markdown(text):
    """
    Removes Markdown triple backticks and language specifiers from a JSON string.
    
    Args:
    text (str): The string that may contain JSON data wrapped in Markdown syntax.
    
    Returns:
    str: The cleaned string, ready for JSON parsing.
    """
    # Pattern to match Markdown fenced code block with optional language (json)
    pattern = r'^```(?:json)?\s*([\s\S]*?)\s*```$'
    
    # Search for the pattern and extract the JSON part
    match = re.search(pattern, text, re.MULTILINE)
    if match:
        # Return only the JSON part without the Markdown code block syntax
        return match.group(1)
    else:
        # Return the original text if no Markdown code block syntax is found
        return text


def extract_summary(html_content):
    
    # Use regular expression to find the SUMMARY section
    summary_match = re.search(r'SUMMARY: ([\s\S]*?)\n\n', html_content)
    
    if summary_match:
        summary_text = summary_match.group(1)
        # Remove all newlines and replace multiple spaces with a single space
        summary_text = re.sub(r'\s+', ' ', summary_text).strip()
        return summary_text
    else:
        return ""


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

