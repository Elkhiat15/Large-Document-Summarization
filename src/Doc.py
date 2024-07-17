import re
from langchain.document_loaders import PyPDFLoader, csv_loader

class Document():
    ID = -1
    def __init__(self):
        Document.ID += 1
        self.data = ""
        self.title = None
        self.summary_ids = []

    def load_from_pdf(self, FilePath):
        loader = PyPDFLoader(FilePath)
        document = loader.load()
        self.extract_data_from_document(document)
    
    def load_from_csv(self, FilePath):
        loader = csv_loader(FilePath)
        document = loader.load()
        self.extract_data_from_document(document)
            
    def extract_data_from_document(self, document):
        text_content = ' '.join([page.page_content for page in document])
        clean_text = self.clean_text(text_content)
        self.data += clean_text
    
    def clean_text(self, text_content):
        text_content = re.sub(r'\t|[ ]{2,}', ' ', text_content)
        #Remove space after '\n' then replace multible breaklines with only one
        text_content = re.sub(r'\n[ ]', '\n', text_content)
        text_content = re.sub(r'\n{2,}', '\n', text_content)
        return text_content.strip()

    def vectorize(self, document):
        pass
    
    def save_to_vector_db(self, document):
        pass

    def summerize(self, document):
        pass
    
    def refine_summary(self):
        pass

    def guid_refine_summary(self, rule):
        pass


doc = Document()
doc.load_from_pdf('Books/the-story-of-doctor-dolittle.pdf')
print(doc.data[0])