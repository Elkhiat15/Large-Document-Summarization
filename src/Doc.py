import re
from langchain.document_loaders import PyPDFLoader, csv_loader
from Embedding import generate_embedding

class Document():
    ID = -1
    def __init__(self):
        Document.ID += 1
        self.data = ""
        self.title = None

    def load_from_pdf(self, FilePath):
        '''
            Loads a PDF document from a file and extracts its data.
            
                Parameters:
                    FilePath (str): A path to the book.
            
                Returns:
                    None
       '''        
        loader = PyPDFLoader(FilePath)
        document = loader.load()
        self.extract_data_from_document(document)
    
    def extract_data_from_document(self, document):
        '''
            Extracts the text data from all pages of the document and combines them after cleaning .
            
                Parameters:
                    document (document): A document that holds the book.
            
                Returns:
                    None
       '''        
        text_content = ' '.join([page.page_content for page in document])
        clean_text = self.clean_text(text_content)
        self.data += clean_text
    
    def clean_text(self, text_content):
        '''
            Cleans the text by removing extra whitespaces and breaklines.
            
                Parameters:
                    text_content (str): The whole text of the document.
            
                Returns:
                    cleaned_text (str): the cleaned text to be processed 
       '''        
        text_content = re.sub(r'\t|[ ]{2,}', ' ', text_content)
        text_content = re.sub(r'\n[ ]', '\n', text_content)
        text_content = re.sub(r'\n{2,}', '\n', text_content)
        cleaned_text = text_content.strip()
        return cleaned_text

    def vectorize(self, text, task):
        return generate_embedding(open_source=False, text=text, task=task)
    
    def save_to_vector_db(self, document):
        # store each document embeddings in a vector db
        pass

    def summerize(self, document):
        # do the summerization
        pass
    
    def refine_summary(self):
        # ask to refine the summary
        pass

    def guid_refine_summary(self, rule):
        # ask to refine the summary with a given rule
        pass
