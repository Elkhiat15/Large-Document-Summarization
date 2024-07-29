import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def get_vectorstore(chunks, use_open_source = False):
    '''
        Creates the vector database and uploads the text chuncks to it.
        
            Parameters:
                use_open_source (bool): a boolean variable to decide using open source embedding or closed source
                                        open source embedding model => HuggingFaceEmbeddings.
                                        closed sourse embedding model => GoogleGenerativeAIEmbeddings.
        
            Returns:
                vectorstore (FAISS]): A vector database that holds the data.
    '''        

    embeddings = HuggingFaceEmbeddings() if use_open_source else GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore