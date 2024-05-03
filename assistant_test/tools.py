#****************************************************************************************************
# A set of tools for assisting with Regulatory Filings
#****************************************************************************************************


#****************************************************************************************************
# Import libraries
#****************************************************************************************************
import os
import json
import html2text
import requests
import pandas as pd

#****************************************************************************************************
# Functions (Tools for the Chat Assistant)
#****************************************************************************************************
{
  "name": "get_list_of_dockets",
  "description": "Retrieves a list of dockets.",
  "parameters": {
    "type": "object",
    "properties": {
      "agencyId": {
        "type": "string",
        "description": "The agency acronym to filter results. Example: 'EPA'"
      },
      "searchTerm": {
        "type": "string",
        "description": "The term to filter results."
      },
      "postedDate": {
        "type": "string",
        "description": "The posted date to filter results. The value must be formatted as yyyy-MM-dd."
      },
      "beforePostedDate": {
        "type": "string",
        "description": "The date before which the dockets were posted. The value must be formatted as yyyy-MM-dd."
      },
      "afterPostedDate": {
        "type": "string",
        "description": "The date after which the dockets were posted. The value must be formatted as yyyy-MM-dd."
      }
    },
    "required": [
      ""
    ]
  }
}

def get_list_of_dockets(agencyId=None, searchTerm=None, postedDate=None, beforePostedDate=None, afterPostedDate=None):
    """
    Retrieves a list of dockets from regulations.gov based on the specified parameters.

    Parameters:
        agencyId (str): The agency acronym to filter results. Example: 'EPA'
        searchTerm (str): The term to filter results.
        postedDate (str): The posted date to filter results. The value must be formatted as yyyy-MM-dd.
        beforePostedDate (str): The date before which the dockets were posted. The value must be formatted as yyyy-MM-dd.
        afterPostedDate (str): The date after which the dockets were posted. The value must be formatted as yyyy-MM-dd.
    """
    """Fetch proposed rules from the API based on the provided filters."""

    url = "https://api.regulations.gov/v4/documents"
    params = {
        "api_key": "4p2Hpwlq1SJ5kOhayfhqeI0D1RtDOo70d8azejwL",
        "filter[documentType]": "Proposed Rule",    # Only fetch proposed rules
        "sort": "-postedDate"                       # Sort by posted date in descending order
    }

    # Add optional filters
    if agencyId:
        params["filter[agencyId]"] = agencyId
    if searchTerm:
        params["filter[searchTerm]"] = searchTerm
    if postedDate:
        params["filter[postedDate]"] = postedDate
    if beforePostedDate:
        params["filter[postedDate][le]"] = beforePostedDate
    if afterPostedDate:
        params["filter[postedDate][ge]"] = afterPostedDate

    # For debugging: Print the full URL and parameters
    print("Making API Call to:", url)
    print("With parameters:", params)


    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("API Call Successful!")
        json_data = response.json()
        return json_data

        # Select only the relevant fields from the response
        # if 'data' in json_data:
        #     df = pd.json_normalize(json_data['data'])
        #     df = df.rename(columns={
        #         'attributes.postedDate': 'Posted Date',
        #         'attributes.title': 'Title',
        #         'id': 'Document ID',
        #         'attributes.commentStartDate': 'Comments Start',
        #         'attributes.commentEndDate': 'Comments End'
        #     })
        #     df['Posted Date'] = pd.to_datetime(df['Posted Date']).dt.strftime('%Y-%m-%d')
        #     df['Comments Start'] = pd.to_datetime(df['Comments Start']).dt.strftime('%Y-%m-%d')
        #     df['Comments End'] = pd.to_datetime(df['Comments End']).dt.strftime('%Y-%m-%d')
        # return df

    else:
        print("API Call Failed!")
        return "API Call Failed!"



# Test
# print(get_available_xbrl_keys_for_filing("0000950170-23-035122"))  
#print(gather_data_from_xbrl_in_json("0000950170-23-035122","StatementsOfIncome/EarningsPerShareDiluted"))  

# print(get_available_xbrl_keys_for_filing("0000320193-22-000108"))    
# function=Function(arguments='{"accession_number": "0000950170-23-035122"}', name='get_available_xbrl_keys_for_filing'), type='function')
# function=Function(arguments='{"accession_number": "0001564590-22-026876"}', name='get_available_xbrl_keys_for_filing'), type='function')
# function=Function(arguments='{"accession_number": "0000320193-23-000106"}', name='get_available_xbrl_keys_for_filing'), type='function'), 
# function=Function(arguments='{"accession_number": "0000320193-22-000108"}', name='get_available_xbrl_keys_for_filing'), type='function')]
