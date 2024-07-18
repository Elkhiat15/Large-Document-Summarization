from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

def generate_embedding(open_source: bool, text: str, task: str = "summarization"):
    """
    Generate embeddings for the provided text using either Google Generative AI or Hugging Face models.

    This function chooses the embedding model based on the `open_source` flag. If `open_source` is False,
    it uses Google Generative AI embeddings; otherwise, it uses Hugging Face embeddings.

    Parameters:
    open_source (bool): Flag to determine which embedding model to use. If False, Google Generative AI is used.
                        If True, Hugging Face is used.
    text (str): The input text to be embedded.
    task (str): The task for which the embedding is being generated, e.g., "classification", "summarization".
                Default is "summarization".

    Returns:
    list: A list of embeddings for the input text.
    """
    if not open_source:
        return generate_embedding_google(text)
    
    return embed_with_hugging_face(text, task=task)

def generate_embedding_google(text: str):
    """
    Generate embeddings for the provided text using Google Generative AI Embeddings.

    This function splits the input text into chunks and generates embeddings for each chunk.

    Parameters:
    text (str): The input text to be embedded.

    Returns:
    list: A list of embeddings for the input text chunks.
    """
    load_dotenv()
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "\t"], 
        chunk_size=6000,
        chunk_overlap=500
    )

    docs = text_splitter.create_documents([text])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectors = embeddings.embed_documents([x.page_content for x in docs])
    return docs, vectors

def embed_with_hugging_face(text: str, task: str):
    """
    Generate embeddings for the provided text using Hugging Face models.

    This function uses Hugging Face Sentence transforemer embeddings to generate embeddings for a given text. 
    It ensures the maximum sequence length aligns with requirements or handles text chunking if necessary.

    Parameters:
    text (str): The input text to be embedded.
    task (str): The task for which the embedding is being generated, e.g., "classification", "summarization".

    Returns:
    list: A list of embeddings for the input text.
    """

    max_seq_length = 512  # This should match the model's maximum sequence length

    # Split text into chunks that do not exceed the max_seq_length
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "\t"],
        chunk_size=max_seq_length,
        chunk_overlap=150  
    )

    docs = text_splitter.create_documents([text])

    
    try:
        embeddings = HuggingFaceEmbeddings()
    except ImportError as e:
        print(e)
        return

    # Generate embeddings for each chunk and concatenate them
    vectors = embeddings.embed_documents([x.page_content for x in docs])
    
    return vectors
