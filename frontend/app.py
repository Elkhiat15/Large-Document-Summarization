import streamlit as st
import summarizer_UI, QA_UI
from streamlit_modal import Modal
from pathlib import Path
from PIL import Image
from PyPDF2 import PdfReader
import os
import sys
sys.path.insert(0, '../src')
import Doc , Embedding as emb ,VectorDB as db
from chat import get_conversation_chain, question_anwering


st.set_page_config(
    page_title="LDS_QA",
    page_icon=":books:",
    layout="wide"
    )

# a boolean variable to check if the summarize button was clicked 
if 'sum' not in st.session_state:
    st.session_state.sum = False

# a boolean variable to check if the QA button was clicked
if 'QA' not in st.session_state:
    st.session_state.QA = False

# a boolean variable to check if the process button was clicked
if 'flag' not in st.session_state:
    st.session_state.flag = False

# a session_state that holds chunking docs --> for summarization
if 'docs' not in st.session_state:
    st.session_state.docs = []

# a session_state that holds vector embeddings
if 'vecs' not in st.session_state:
    st.session_state.vecs = list[list[float]]

# a session_state that holds chunking text --> for QA 
if 'chunks' not in st.session_state:
    st.session_state.chunks = []

# current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the assets
cover_dir = os.path.join(current_dir, '..', 'assets', 'cover.jpg')

cover = Image.open(cover_dir)
dummy_dir = os.path.join(current_dir, '..', 'assets', 'left.jpg')

dummy = Image.open(dummy_dir)

st.header("Let's Get Started!")
st.image(image=cover, caption="cover")
_, c, _ = st.columns(spec=[1,5,1]) # to center the subheader
c.subheader(":blue[Please, Upload Pdf documents that have [5-2000] pages in total.]")
files = st.file_uploader(label="Uploader", accept_multiple_files=True, type="pdf", label_visibility="collapsed")

process = st.button(label="Process")

doc = Doc.Document()

if not files:
    st.session_state.flag = False
    st.session_state.started = False
    st.session_state.guided_refined = False
    st.session_state.auto_refined = False
    st.session_state.add_more = False
    st.session_state.response = ""
    st.session_state.docs = []
    st.session_state.chunks = []
    st.session_state.vecs = list[list[float]]
   
if process:
    if not files:
        st.error("Please, Upload Pdf documents")
    else:
        total_lenght = 0 
        exceeded = False
        for file in files:
            pdf_reader = PdfReader(file)
            total_lenght+=len(pdf_reader.pages)
            if(total_lenght > 2000):
                st.warning("Please, upload Pdf documents that have less than 2000 pages in total")
                exceeded = True
                break
            doc.extract_data_from_document(pdf_reader)
        if not exceeded:           
            with st.spinner("Processing ..."):
                open_source = False
                st.session_state.chunks, st.session_state.docs, st.session_state.vecs = emb.generate_embedding(open_source, doc.data)
                st.session_state.vectorstore =  db.get_vectorstore(st.session_state.chunks, open_source)

            st.success(f"Processing Done! **{total_lenght}** pages to be summarized")
            st.session_state.flag = True       

if files and st.session_state.flag:      
    c1, c2 = st.columns(spec=[1,1], gap="small")
    with c1:
        st.image(image=dummy)
        _, c, _ = c1.columns(spec=[1,1,1])
        with c:
            if st.button("Summarize Pdfs"):
                st.session_state.sum = True
                st.session_state.QA = False
    with c2:
        st.image(image=dummy)
        _, c, _ = c2.columns(spec=[1,1,1])
        with c:
            if st.button("Chat with Pdfs"):
                st.session_state.QA = True
                st.session_state.sum = False
                st.session_state.add_more = False
                st.session_state.auto_refined = False
                st.session_state.guided_refined = False


class MaltiPage:
    def run():
        if st.session_state.flag:
            if st.session_state.sum:
                summarizer_UI.run(st,st.session_state.docs ,st.session_state.vecs, PdfReader)
            if  st.session_state.QA:
                chain = get_conversation_chain(st.session_state.vectorstore, temperature=0.7)
                QA_UI.run(st, chain, question_anwering)
        else:
            st.session_state.QA = False
            st.session_state.sum = False

## run the program     
    run()