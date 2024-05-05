import json

# Document initially without 'search_terms' in expert details
document = {
  "analysis_title": "Analysis of the Proposed ITAR Exemption for AUKUS Partnership",
  "sections": [
    {
      "title": "Background of AUKUS Partnership",
      "description": "Details the origins and goals of the AUKUS partnership and its significance in enhancing trilateral security cooperation.",
      "token": "background_aukus",
      "consult_experts": [
        {
          "expert_type": "Political",
          "specialized_knowledge": "International Relations and Security Alliances",
          "reason_for_request": "To provide context on the geopolitical implications of the AUKUS partnership."
        }
      ]
    }
    # Other sections can be added here
  ]
}

def generate_search_terms(expert_type, specialized_knowledge):
    # Placeholder for the real function that generates search terms based on expert's details
    # Here you'd replace this logic with your black box function.
    if expert_type == "Political":
        return ["geopolitics", "international relations", "security alliances"]
    return []

def add_search_terms_to_document(document):
    for section in document['sections']:
        for expert in section['consult_experts']:
            # Generate and insert search terms for each expert
            expert['search_terms'] = generate_search_terms(expert['expert_type'], expert['specialized_knowledge'])

def print_document(document):
    print(json.dumps(document, indent=4))

# Example Usage:
add_search_terms_to_document(document)
print_document(document)  # To display the document with search terms