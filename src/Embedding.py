from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()
def chunck(text, size, overlap):
    '''
        Chunk a text into documents
        based on newline characters and a specified chunk size.

            Parameters:
                text (str): The input text to be chunked.
                size (int): The maximum size of each chunk in characters.
                overlap (int): the number of overlapping.

            Returns:
                text_chuncks (list[str]): A list of string, each containing a chunk of the input text
                docs (list[Document]): A list of documents, each containing a chunk of the input text.
    '''

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "\t"], 
        chunk_size=size,
        chunk_overlap=overlap
    )

    text_chuncks = text_splitter.split_text(text)
    docs = text_splitter.create_documents([text])
    return text_chuncks, docs

def generate_embedding(open_source, text):
    '''
        Generate embeddings for the provided text using either Google Generative AI or Hugging Face models.

        This function chooses the embedding model based on the `open_source` flag. If `open_source` is False,
        it uses Google Generative AI embeddings; otherwise, it uses Hugging Face embeddings.

            Parameters:
                open_source (bool): Flag to determine which embedding model to use. If False, Google Generative AI is used.
                                    If True, Hugging Face is used.
                text (str): The input text to be embedded.

            Returns:
                another function calling.
    '''

    if not open_source:
        return generate_embedding_google(text)
    
    return embed_with_hugging_face(text)

def generate_embedding_google(text: str):
    '''
        Generate embeddings for the provided text using Google Generative AI Embeddings.
        This function splits the input text into chunks and generates embeddings for each chunk.

            Parameters:
                text (str): The input text to be embedded.

            Returns:
                text_chuncks (list[str]): A list of string, each containing a chunk of the input text
                docs (list[Document]): A list of documents, each containing a chunk of the input text.
                vectors (list[list[float]]): A list of embeddings for the input text chunks.
    '''
    
    text_chunk, docs = chunck(text, size=6000, overlap=500)  
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectors =embeddings.embed_documents([x.page_content for x in docs])
    return text_chunk, docs, vectors

def embed_with_hugging_face(text):
    '''
        Generate embeddings for the provided text using Hugging Face models.

        This function uses HuggingFace Sentence transforemer embeddings to generate embeddings for a given text. 
        It ensures the maximum sequence length aligns with requirements or handles text chunking if necessary.

            Parameters:
                text (str): The input text to be embedded.
                
            Returns:
                text_chuncks (list[str]): A list of string, each containing a chunk of the input text
                docs (list[Document]): A list of documents, each containing a chunk of the input text.
                vectors (list[list[float]]): A list of embeddings for the input text chunks.
    '''
 
    text_chunk, docs = chunck(text, size=512, overlap=150)  

    try:
        embeddings = HuggingFaceEmbeddings()
    except ImportError as e:
        print(e)
        return

    vectors = embeddings.embed_documents([x.page_content for x in docs])
    return text_chunk, docs, vectors
