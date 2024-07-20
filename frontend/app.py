import streamlit as st
from PyPDF2 import PdfReader
import sys
sys.path.insert(0, '../src')
import Doc

st.set_page_config(
    page_title="LDS_QA",
    page_icon=":books:"
    )

doc = Doc.Document()

st.header("Starter")
files = st.file_uploader(label=":green[Upload PDF files here]", accept_multiple_files=True, type="pdf")

for file in files:
    doc.load_from_pdf(file)
    st.markdown(doc.data[:100])