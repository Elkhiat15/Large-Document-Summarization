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
        # loads from pdf file
        loader = PyPDFLoader(FilePath)
        document = loader.load()
        self.extract_data_from_document(document)
    
    def extract_data_from_document(self, document):
        text_content = ' '.join([page.page_content for page in document])
        clean_text = self.clean_text(text_content)
        self.data += clean_text
    
    def clean_text(self, text_content):
        text_content = re.sub(r'\t|[ ]{2,}', ' ', text_content)
        text_content = re.sub(r'\n[ ]', '\n', text_content)
        text_content = re.sub(r'\n{2,}', '\n', text_content)
        return text_content.strip()

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


doc = Document()
doc.load_from_pdf('Books/the-story-of-doctor-dolittle.pdf')
print(doc.data[0])