# Large Document Summarization and Chat with PDFs

## Overview
This project provides a comprehensive solution for summarizing large documents and interacting with them in a conversational manner. Our application leverages the power of AI to automatically summarize one or more large documents, refine the summaries based on user input, and even engage in chat-like conversations with PDFs.

---
## Key Features

- **Multi-Document Summarization**: Upload one or more large documents and receive a concise summary of the content.  
- **Automatic Summary Refining**: Ask the model to refine the summary automatically for improved response.  
- **Guided Summary Refining**: Provide guidance to the model to refine the summary based on your specific needs.  
- **Cumulative Summarization**: Add more documents to be summarized in a cumulative way, allowing for a comprehensive understanding of multiple documents.  
- **Chat with PDFs**: Engage in conversational interactions with PDFs, exploring their content in a more intuitive and interactive way.

<p align="center">
<img src="assets/LDS_GIF.gif" alt="My Image" style="float: right; margin: 10px;"> 
</p>

<img align="right" width="55%" src="assets/LDS_GIF.gif">

### First feature:

Our summarization workflow involves the following steps:

Document Upload: Upload the document(s) to be summarized.
Text Cleaning: Clean the text to remove unnecessary characters and formatting.
Text Chunking: Break the text into smaller chunks for more efficient processing.
Clustering: Cluster the chunked text to identify key topics and themes.
Centroid Summarization: Summarize the centroids of each cluster to capture the main ideas.
Final Summarization: Summarize the summaries to provide a concise overview of the entire document.
