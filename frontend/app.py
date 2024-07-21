import streamlit as st
import summarizer_UI, QA_UI
from streamlit_modal import Modal
from pathlib import Path
from PIL import Image
from PyPDF2 import PdfReader

import sys
sys.path.insert(0, '../src')
import Doc , Embedding as emb


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

# a session_state that holds chunking docs 
if 'docs' not in st.session_state:
    st.session_state.docs = []

# a session_state that holds vector embeddings
if 'vecs' not in st.session_state:
    st.session_state.vecs = list[list[float]]

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
cover_dir = current_dir / "..\\assets" / "cover.jpg"
cover = Image.open(cover_dir)
dummy_dir = current_dir / "..\\assets" / "left.jpg"
dummy = Image.open(dummy_dir)

st.header("Let's Get Started!")
st.image(image=cover, caption="cover")
_, c, _ = st.columns(spec=[1,1,1]) # to center the subheader
c.subheader(":green[Upload PDF files here]")
files = st.file_uploader(label="Uploader", accept_multiple_files=True, type="pdf", label_visibility="collapsed")

process = st.button(label="Process")

doc = Doc.Document()

if not files:
    st.session_state.flag = False
    st.session_state.docs = []
    st.session_state.vecs = list[list[float]]
if process:
    if not files:
        st.error("Please upload Pdf documents")
    else:
        total_lenght = 0 
        exceeded = False
        for file in files:
            pdf_reader = PdfReader(file)
            total_lenght+=len(pdf_reader.pages)
            if(total_lenght > 2000):
                st.warning("Please upload Pdf documents that have less than 2000 pages in total")
                exceeded = True
                break
            doc.extract_data_from_document(pdf_reader)
        if not exceeded:           
            with st.spinner("Processing ..."):
                # TODO: 3luka-> use vector db to retreive vectors 
                # TODO: 3luka or me-> get docs from one function only
                st.session_state.docs, st.session_state.vecs = emb.generate_embedding(open_source=False, text=doc.data)
                
            st.success("Done!")
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

class MaltiPage:
    def run():
        if st.session_state.flag:
            if st.session_state.sum:
                summarizer_UI.run(st,st.session_state.docs ,st.session_state.vecs)
            if  st.session_state.QA:
                # TODO: 3luka-> pass any parameters that you need inside you function here 
                QA_UI.run(st)
        else:
            st.session_state.QA = False
            st.session_state.sum = False

## run the program     
    run()