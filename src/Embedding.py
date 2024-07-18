from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings

def generate_embeddeing_google(text:str):
    load_dotenv()
    text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "\t"], 
    chunk_size=6000,
    chunk_overlap=500
    )

    docs = text_splitter.create_documents([text])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectors = embeddings.embed_documents([x.page_content for x in docs])
    return vectors

def embed_with_hugging_face(text, task):
    # use this opensource if there is no gemni api is linked
    # need to check max seq length and make sure it alligns with gimini or handle passing the chuck length 
    embeddings = HuggingFaceInstructEmbeddings(
        query_instruction="Represent the query for summarization: "
    )
    return embeddings.embed_query(text)

def generate_embedding(open_source:bool, text:str, task="summarization"):

    if not open_source:
        return generate_embeddeing_google(text)
    
    return embed_with_hugging_face(text, task=task)
    



