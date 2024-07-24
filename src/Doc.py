import re

from PyPDF2 import PdfReader
from Embedding import generate_embedding
from VectorDB import VectorDataBase
import chat

class Document():
    ID = -1
    def __init__(self):
        """
        Initializes a new Document object.

        Attributes:
        -----------
        ID : int
            A class-level attribute that keeps track of the number of Document instances created.
        data : str
            Holds the text data of the document.
        title : str
            Stores the title of the document.
        summaries : list
            A list to store the summaries of the document.

        Returns:
        --------
        None
        """
        Document.ID += 1
        self.data = ""
        self.title = None
        self.summaries = []

    # NOTE: there is no need to this function after stablishing the front end 
    def load_from_pdf(self, pdf):
        '''
        Loads a PDF document from a file and extracts its data.
        
            Parameters:
                FilePath (str): A path to the book.
        
            Returns:
                None
        '''    
        pdf_reader = PdfReader(pdf)    
        self.extract_data_from_document(pdf_reader)
    
    def get_pdf_text(self, pdf):
        text = ""
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def extract_data_from_document(self, pdf_reader):
        '''
        Extracts the text data from all pages of the document and combines them after cleaning .
        
            Parameters:
                document (document): A document that holds the book.
        
            Returns:
                None
        '''        
        text_content = ' '.join([page.extract_text() for page in pdf_reader.pages])
        clean_text = self.clean_text(text_content)
        self.data += clean_text
    
    def clean_text(self, text_content):
        '''
        Cleans the text by removing punctiations, Url links, mails, extra whitespaces and breaklines.
        
            Parameters:
                text_content (str): The whole text of the document.
        
            Returns:
                cleaned_text (str): the cleaned text to be processed 
        '''        

        text_content = re.sub(r'\n[ ]', '\n', text_content)
        text_content = re.sub(r'\n{2,}', '\n', text_content)
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,6})?\b'
        text_content = re.sub(email_pattern, '', text_content)  # remove email addresses
        urls = re.findall(r'https?://\S+', text_content)  # find all URLs
        for url in urls:
            text_content = text_content.replace(url, '')  # remove the URL
        
        text_content = re.sub(r'[^\x00-\x7F]+', '', text_content) # remove non-ASCII characters
        text_content = re.sub(r'[^\w\s]+', '', text_content) # remove some punctuations
        text_content = re.sub(r'\t|[ ]{2,}', ' ', text_content) # remove tabs and multible whitespaces 

        cleaned_text = text_content.strip()
        return cleaned_text

    def vectorize(self, opensource, text, task):
        '''
        Creates embeddings for the given text            
            Parameters:
                text (str): The whole text of the document.
                task (str): The task for which the embeddings summerization, retriva, etc.
                db (DeepLakeDataset): The vector database to save the embeddings.
        
            Returns:
                embeddings (list): the embeddings for the given text
        ''' 
        # NOTE: the generate_embedding returns two variables docs and vectors 
        _ , embeddings = generate_embedding(open_source=opensource, text=text, task=task)
        
        return embeddings 
    
    def save_to_vector_db(self, text, vector_db):
        '''
        Saves the embeddings of the document to the vector database           
            Parameters:
                embeddings(list): vector representation of text document.
                vector_db (DeepLakeDataset): The whole text of the document.
        
            Returns:
                None
        '''
        vector_db = vector_db.add_to_database(text)

    def summerize(self, document):
        '''
        Creates summary of the document given and saves it in the summaries list.           
            Parameters:
                document (str): The whole text of the document.    

            Returns:
                None
        '''  
        pass
    
    def refine_summary(self):
        '''
        Makes the model modify the summary of the document, and adds it to the summary list
  
        '''  

        pass

    def guid_refine_summary(self, rule):
        '''
        Makes the model modify the summary of the document based on a given prompt (rule), and adds it to the summary list
            Parameters:
            rule (str): A prompt string to guide the summary creation.

            Returns:
                None
        '''          
        pass


# db = VectorDataBase(use_open_source=False)
# doc = Document()
# doc.load_from_pdf('Large-Document-Summarization/Books/the-story-of-doctor-dolittle.pdf')
# # # #print(doc.vectorize(opensource=False, text=doc.data, task="summarization"))
# doc.save_to_vector_db(doc.data, db)
# # conv_chain = chat.get_conversation_chain(db, temperature=0.2)
# # print(chat.question_anwering(input_question="What does this book talk about?", conversation_chain=conv_chain))
# db.get_embeddings_text()
# db.delete()
# print(db.VectorStore)