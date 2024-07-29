import re
from PyPDF2 import PdfReader
class Document():
    def __init__(self):
        """
        Initializes a new Document object.

        Attributes:
        -----------
        data : str
            Holds the text data of the document.
        
        Returns:
        --------
        None
        """
        
        self.data = ""
    
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
                pdf_reader (PdfReader): pdf reader that reads the documents.
        
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
