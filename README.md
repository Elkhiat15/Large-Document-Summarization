# Large Document Summarization and Chat with PDFs

## Overview
This project provides a comprehensive solution for summarizing large documents and interacting with them in a conversational manner. Our application leverages the power of AI to automatically summarize one or more large documents, refine the summaries based on user input, and even engage in chat-like conversations with PDFs.

---
## Technical Details
<img width="75px" src="assets/langchain.jpeg" alt="Langchain Icon" />   <img width="75px" src="assets/python-icon.svg" alt="Python Icon" />   <img width="75px" src="assets/google-gemini-icon.svg" alt="Gemini Icon" />   <img width="75px" src="assets/streamlit-icon.svg" alt="Streamlit Icon" />

### Our application is built using the following technologies:

[**Python**](https://www.python.org/): The primary programming language used for development.  
[**Langchain**](https://www.langchain.com): A powerful library for natural language processing tasks.  
[**Gemini API**](https://ai.google.dev/gemini-api/docs): An LLM API that I used for summarization and Embedding.  
[**FAISS**](https://faiss.ai/): A library for efficient similarity search and clustering.  
[**Streamlit**](https://streamlit.io/): A popular framework for building and deploying web applications.  

---
## Key Features

- [**Multi/Large Document Summarization**](#f1): Upload one or more large documents and receive a concise summary of the content.  
- [**Automatic Summary Refining**](#f2): Ask the model to refine the summary automatically for improved response.  
- [**Guided Summary Refining**](#f3): Provide guidance to the model to refine the summary based on your specific needs.  
- [**Cumulative Summarization**](#f4): Add more documents to be summarized in a cumulative way, allowing for a comprehensive understanding of multiple documents.  
- [**Chat with PDFs**](#f5): Engage in conversational interactions with PDFs, exploring their content in a more intuitive and interactive way.
---

## How to use
### To get started with our application, simply follow these steps:

* Clone the repository and replace `<REPO_LINK>` by the link to clone 
```
git clone <REPO_LINK>
```  
* Install the required dependencies using
* Run the application using
```
pip install -r requirements.txt
streamlit run main.py
```  
* You may need to change API Key, you can replace the `<YOUR_KEY>` with you actual API key in `.env` file in `src` directory.
```
GOOGLE_API_KEY = <YOUR_KEY>
```  
---
<a name="f1"></a>
# Usage
## 1) Multi/Large Document Summarization

<p align="center">
<img src="assets/LDS.jpeg" alt="My Image" > 
</p>

### Our summarization workflow involves the following steps:

**Document Upload**: Upload the document(s) to be summarized.  
**Text Cleaning**: Clean the text to remove unnecessary characters, links and formatting.  
**Text Chunking**: Break the text into smaller chunks for more efficient processing.  
**Clustering**: Cluster the chunked text to identify key topics and themes.   
**Centroid Summarization**: Summarize the centroids of each cluster to capture the main ideas.  
**Final Summarization**: Summarize the summaries to provide a concise overview of the entire document.  

<p align="center">
<img src="assets/LDS_GIF.gif" alt="My Image"> 
</p>

---
<a name="f2"></a>
## 2) Automatic Summary Refining

---

<a name="f3"></a>
## 3) Guided Summary Refining

---

<a name="f4"></a>
## 4) Cumulative Summarization

---

<a name="f5"></a>
## 5) Chat with PDFs

---
