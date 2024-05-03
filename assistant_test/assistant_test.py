#************************************************************************************************
# Imports
#************************************************************************************************
import os
from dotenv import load_dotenv
import pandas as pd
from openai import AzureOpenAI
import json
import time

# Import the assistant tools
from tools.faaa_researcher import get_sections_of_data_available_in_last_10K_filing, get_data_from_last_10K_filing_by_section

#************************************************************************************************
# Load environment variables from a .env file and set local variables
#************************************************************************************************
load_dotenv()

AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
FAAA_ASSISTANT_ID = os.getenv("FAAA_ASSISTANT_ID")


#************************************************************************************************
# Create client instance of the AzureOpenAI class
#************************************************************************************************
AOAI = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_API_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION
        )

#************************************************************************************************
# Setup utility functions
#************************************************************************************************

# Pretty printing JSON
def show_json(obj):
    print(json.dumps(json.loads(obj.model_dump_json()), indent=4))

# Pretty printing messages
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = AOAI.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)  
        time.sleep(0.5)
    return run

def submit_message(assistant_id, thread, user_message):
    AOAI.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_message)
    return AOAI.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)

def get_response(thread):
    return AOAI.beta.threads.messages.list(thread_id=thread.id, order="asc")

def create_thread_and_run(user_input):
    thread = AOAI.beta.threads.create()
    run = submit_message(FAAA_ASSISTANT_ID, thread, user_input)
    return thread, run

