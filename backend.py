import requests
import json
import random

# This is small database of legal cases for the RAG Lawyer.
LEGAL_DATABASE = [
    {
        "case_text": "In a landmark case, a man sued a parrot for defamation after the bird repeated insults it heard from its owner. The court ruled that a non-human entity cannot be held liable for defamation.",
        "citation": "Smith v. Talking Pets (1994)",
        "metadata": {
            "case_type": "Defamation",
            "jurisdiction": "US",
            "year": 1994,
            "key_legal_principles": ["Libel", "Defamation", "Intent", "Liability"],
            "outcome": "Dismissed"
        }
    },
    {
        "case_text": "The case involved a dispute over a fence that a neighbor built 2 inches onto the plaintiff's property. The court cited the legal principle of 'adverse possession,' but ultimately ruled in favor of the plaintiff, stating the encroachment was not substantial enough to warrant a transfer of land.",
        "citation": "Davis v. Thompson (2001)",
        "metadata": {
            "case_type": "Property Dispute",
            "jurisdiction": "UK",
            "year": 2001,
            "key_legal_principles": ["Property Law", "Adverse Possession", "Easements"],
            "outcome": "Guilty"
        }
    },
    {
        "case_text": "A case of negligence where a company failed to properly secure a warehouse door, leading to a break-in and theft. The court established that the company had a 'duty of care' to protect its property and was therefore negligent.",
        "citation": "Corpco v. State of New York (2018)",
        "metadata": {
            "case_type": "Negligence",
            "jurisdiction": "US",
            "year": 2018,
            "key_legal_principles": ["Duty of Care", "Negligence", "Breach of Contract"],
            "outcome": "Guilty"
        }
    },
    {
        "case_text": "A celebrity sued a media outlet for publishing a satirical article. The court found that the article was protected under the principle of 'parody' and 'fair use,' and was not intended to be taken as factual defamation.",
        "citation": "Celebrity v. Tabloid Press (2020)",
        "metadata": {
            "case_type": "Defamation",
            "jurisdiction": "EU",
            "year": 2020,
            "key_legal_principles": ["Defamation", "Parody", "Fair Use", "Freedom of Speech"],
            "outcome": "Dismissed"
        }
    },
    {
        "case_text": "A man accidentally left his pet snail on the property of a neighbor, who then claimed ownership. The court ruled that a pet snail could be considered 'abandoned property' and that the neighbor was within his rights to claim it.",
        "citation": "Snail v. Escargot (2022)",
        "metadata": {
            "case_type": "Property Dispute",
            "jurisdiction": "US",
            "year": 2022,
            "key_legal_principles": ["Property Law", "Abandonment of Property"],
            "outcome": "Settled"
        }
    }
]

# This function sends a message to the AI and gets a response.
def call_gemini_api(prompt, api_key):
    # This is the address for the AI.
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # Try to send the request and get a response.
    try:
        response = requests.post(API_URL + "?key=" + api_key, headers=headers, data=json.dumps(payload))
        
        # If the request was not successful, it will give us an error.
        response.raise_for_status() 
        
        result = response.json()
        
        # Check if the response from the AI is what we expect.
        if result and 'candidates' in result and result['candidates'][0]['content']['parts']:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Error: Invalid AI response format."
    except Exception as e:
        # If something went wrong, we'll return an error message.
        print(f"Failed to get a response from the API: {e}")
        return "An error occurred with the API. Please try again later."

# This function creates a new random case for the trial.
def generate_case():
    cases = [
        "A man sues a parrot for defamation after it publicly mocked his singing.",
        "A squirrel is charged with trespassing after it steals a priceless diamond from a museum.",
        "A company is accused of negligence for not putting a 'wet floor' sign in a puddle caused by a leaky ceiling.",
        "A rogue AI is on trial for plagiarism after it wrote a novel that was suspiciously similar to a famous classic."
    ]
    return random.choice(cases)

# This function finds the best matching case from our database.
def hybrid_retrieval(query):
    query_lower = query.lower()
    
    best_match = None
    
    for doc in LEGAL_DATABASE:
        doc_text_lower = doc['case_text'].lower()
        metadata = doc['metadata']
        
        # Check if any keywords from the case are in our database.
        for word in query_lower.split():
            if len(word) > 3 and word in doc_text_lower:
                best_match = doc
                break
        
        if best_match is not None:
            break

        # Also check if any legal principles match.
        if metadata['case_type'].lower() in query_lower:
            best_match = doc
            break
        
        for principle in metadata['key_legal_principles']:
            if principle.lower() in query_lower:
                best_match = doc
                break
        
        if best_match is not None:
            break

    return best_match