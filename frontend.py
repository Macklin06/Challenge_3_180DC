import streamlit as st

# This function is like a designer for our app! It decides where everything goes.
def render_ui():
    # We use st.markdown to add a title and a subtitle, and we can use HTML to make them look nice.
    st.markdown("<h1 style='text-align: center; color: #4F46E5;'>Courtroom Clash ⚖️</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #E5E7EB;'>AI Lawyers Battle It Out!</h3>", unsafe_allow_html=True)
    st.divider()

    # This is a box to hold our case scenario. It has a border to make it stand out.
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center;'>Case Scenario</h4>", unsafe_allow_html=True)
        # Show the current case scenario from our app's memory.
        st.markdown(f"<p style='text-align: center; font-size: 20px; font-style: italic; color: #D1D5DB;'>{st.session_state.case_scenario}</p>", unsafe_allow_html=True)

    st.divider()

    # creating two columns so we can put the lawyers side by side.
    col1, col2 = st.columns(2)

    with col1:
        # This is a box for the RAG Lawyer.
        with st.container(border=True):
            st.subheader("RAG Lawyer")
            # We show the RAG Lawyer's argument.
            st.markdown(f"**Argument:** {st.session_state.rag_argument}")
            
            # If the RAG Lawyer found a case, we'll show the citation and metadata.
            if st.session_state.rag_citation:
                st.markdown(f"**Citation:** `{st.session_state.rag_citation}`")
                st.markdown(f"**Metadata:**")
                st.json(st.session_state.rag_metadata)
                
    with col2:
        # This is a box for the Chaos Lawyer.
        with st.container(border=True):
            st.subheader("Chaos Lawyer")
            # We show the Chaos Lawyer's silly argument.
            st.markdown(f"**Argument:** {st.session_state.chaos_argument}")
            st.markdown(f"**Rhetoric:** *If a tree falls in the forest, does a squirrel have standing?!*")

    st.divider()

    # This is the section for the judge to see the verdict and control the trial.
    st.subheader("Judge's Panel")
    # We show the current verdict message.
    st.markdown(f"<p style='text-align: center; font-weight: bold;'>{st.session_state.verdict}</p>", unsafe_allow_html=True)

    # create three columns for our buttons.
    col3, col4, col5 = st.columns(3)
    
    # return the columns so our main app file can put buttons inside them.
    return col3, col4, col5
