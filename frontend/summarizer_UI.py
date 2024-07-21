import sys
import time

import streamlit as st 
sys.path.insert(0, '../src')
import summerize


# TODO: handle small text
def run(stt, docs, vectors):
       def stream_data():
              for word in response.split(" "):
                     yield word + " "
                     time.sleep(0.035)

       st.header("Welcome to Summarizer")

       response = ""
       num_clusters = 5
       if len(docs) < num_clusters:
              response = "The documents is too short to be summarized"
       else :
              with st.spinner("Processing ..."):
                     response = summerize.summarize(num_clusters, docs, vectors)
       
       if 'add' not in st.session_state:
              st.session_state.add = False


       st.write_stream(stream_data)
       st.session_state.done = True