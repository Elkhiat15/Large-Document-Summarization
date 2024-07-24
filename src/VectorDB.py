import os
from dotenv import load_dotenv
from langchain_community.vectorstores import DeepLake
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from Embedding import chunck


class VectorDataBase:

    def __init__(self, use_open_source=False):
        """
            Initialize VectorDataBase instance.

            This function initializes a VectorDataBase instance with the specified parameters.
            It loads environment variables using dotenv, sets the dataset path, and initializes
            the vector database (DeepLake) with the appropriate embedding model based on the
            'use_open_source' flag.

                Parameters:
                    use_open_source (bool): A flag indicating whether to use an open-source embedding model.
                                            If True, HuggingFaceEmbeddings will be used; otherwise,
                                            GoogleGenerativeAIEmbeddings will be used.
                                            Default is False.

                Returns:
                    None
        """
        load_dotenv()
        self.use_open_source = use_open_source
        self.dataset_path = 'hub://muhammadmahmoud01/vector_db_HugeDoc'
        self.VectorStore = DeepLake(self.dataset_path, overwrite=True, 
                           embedding=HuggingFaceEmbeddings() if use_open_source else GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
    
    def add_to_database(self,text):
        """
            Add documents to the vector database.

            This function takes a text input, splits it into smaller chunks based on the specified parameters,
            and adds these chunks as documents to the vector database. The chunk size and overlap are determined
            based on the 'use_open_source' flag.

                Parameters:
                    text (str): The input text to be added to the vector database.

                Returns:
                    None
        """
        docs = chunck(text, 
                      size=512 if self.use_open_source else 6000, 
                      overlap=150 if self.use_open_source else 500)
        self.ids = self.VectorStore.add_documents(docs)
    
    def get_ids(self):
        return self.ids