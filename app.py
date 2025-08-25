import streamlit as st
import random
from frontend import render_ui
from backend import call_gemini_api, generate_case, hybrid_retrieval


# Set up the webpage
st.set_page_config(page_title="Courtroom Clash", layout="centered")

# Set up some variables to store information as the user interacts with the app
if 'case_scenario' not in st.session_state:
    st.session_state.case_scenario = "Press 'Start Trial' to begin the case."
    st.session_state.rag_argument = "Ready to present a fact-based argument..."
    st.session_state.chaos_argument = "Ready to unleash chaos..."
    st.session_state.verdict = ""
    st.session_state.rag_citation = ""
    st.session_state.rag_metadata = {}

# Ask for an API key in a sidebar so the user can paste it there.
with st.sidebar:
    st.title("API Key")
    api_key = st.text_input("Enter your Google API Key", type="password")

def debate(api_key):
    # Set the text to show the trial is in progress
    st.session_state.verdict = "The trial is in session..."
    st.session_state.rag_argument = "Thinking..."
    st.session_state.chaos_argument = "Thinking..."

    # The RAG lawyer is a smart lawyer who uses a database.
    #shows a spinner while they are "thinking."
    with st.spinner('RAG Lawyer is building a case...'):
        relevant_case = hybrid_retrieval(st.session_state.case_scenario)
        rag_prompt = "You are a fact-based lawyer presenting a prosecution argument. Argue for the prosecution in the following case: " + st.session_state.case_scenario
        
        if relevant_case is not None:
            rag_prompt += " Use the following legal precedent and information to support your argument: " + relevant_case['case_text'] + ". The argument must be grounded in this evidence and cite the case properly."
            st.session_state.rag_citation = relevant_case['citation']
            st.session_state.rag_metadata = relevant_case['metadata']
        else:
            rag_prompt += " No direct legal precedent has been found, so you must argue based on general legal principles."
            st.session_state.rag_citation = "No direct precedent found."
            st.session_state.rag_metadata = {}
            
        st.session_state.rag_argument = call_gemini_api(rag_prompt, api_key)
        
    # The Chaos lawyer is a silly lawyer who makes things up.
    # shows another spinner for them.
    with st.spinner('Chaos Lawyer is improvising a defense...'):
        chaos_prompt = "You are a completely absurd and creative lawyer representing the defense. Your client is on trial for the case: " + st.session_state.case_scenario + ". Your goal is to win through sheer nonsense and rhetorical flair, ignoring all facts and legal precedents. Generate an exaggerated and ridiculous argument. Do not use a citation."
        st.session_state.chaos_argument = call_gemini_api(chaos_prompt, api_key)

    # After both lawyers are done, update the verdict message.
    st.session_state.verdict = "Arguments presented. Judge, please deliver your verdict!"

# This function starts a new trial.
def start_trial(api_key):
    st.session_state.case_scenario = generate_case()
    debate(api_key)

# This function handles what happens when a lawyer wins, or if there is no winner.
def give_verdict(winner):
    if winner == 'RAG':
        st.session_state.verdict = "RAG Lawyer wins the case! Justice prevails!"
    elif winner == 'CHAOS':
        st.session_state.verdict = "Chaos Lawyer wins! The court is in pandemonium!"
    else:
        st.session_state.verdict = "The Judge declares a hung jury. No verdict is reached."

# This function introduces new evidence to the case.
def introduce_evidence(api_key):
    new_evidence = [
        "New evidence: The parrot claims it was framed!",
        "New evidence: A hidden clause in the property deed allows for a squirrel to be the sole heir.",
        "New evidence: The leaky ceiling was a deliberate act by a rival company.",
        "New evidence: The rogue AI was simply trying to express itself through interpretive dance."
    ]
    st.session_state.case_scenario = random.choice(new_evidence)
    debate(api_key)

# call the function that draws all the buttons and text on the screen.
col3, col4, col5 = render_ui()

# set up what happens when the buttons are clicked.
with col4:
    if st.button("Start Trial", use_container_width=True):
        if not api_key:
            st.error("Please enter your API key in the sidebar to start the trial.")
        else:
            start_trial(api_key)

# verdict buttons
st.divider()
st.subheader("Judge's Ruling")
col_verdict1, col_verdict2, col_verdict3 = st.columns(3)

with col_verdict1:
    st.button("RAG Wins", on_click=lambda: give_verdict('RAG'), use_container_width=True, type="primary")

with col_verdict2:
    st.button("Chaos Wins", on_click=lambda: give_verdict('CHAOS'), use_container_width=True, type="primary")

with col_verdict3:
    st.button("No Verdict", on_click=lambda: give_verdict('NO_VERDICT'), use_container_width=True, type="secondary")

st.button("Introduce New Evidence", on_click=lambda: introduce_evidence(api_key), use_container_width=True)