import streamlit as st 
import sys
sys.path.insert(0, '../src')
import summerize

# TODO: handle small text
def run(stt, docs, vectors):
       st.header("Welcome to Summarizer")

       num_clusters = 5
       response = ""
       with st.spinner("Processing ..."):
              response = summerize.summarize(num_clusters, docs, vectors)
       st.markdown(response, unsafe_allow_html=True) 
