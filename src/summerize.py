import Doc, Embedding as emb
import numpy as np

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.chains.summarize import load_summarize_chain
from sklearn.cluster import KMeans
from dotenv import load_dotenv

def get_indices(num_clusters, kmeans):
    closest_indices = []

    for i in range(num_clusters):
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append(closest_index)
        selected_indices = sorted(closest_indices)
    
    return selected_indices

def get_summaries(map_chain, selected_indices, docs):
    selected_docs = [docs[idx] for idx in selected_indices]

    summary_list = []
    for i, doc in enumerate(selected_docs):
        chunk_summary = map_chain.invoke([doc])
        summary_list.append(chunk_summary['output_text'])

    summaries = "\n".join(summary_list)
    summaries = Document(page_content=summaries)
    return summaries

def cluster_and_summarize(num_clusters):
    kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(vectors)

    selected_indices = get_indices(num_clusters, kmeans)

    map_prompt = """
    You will be given a single passage of a book. This section will be enclosed in triple backticks (```)
    Your goal is to give a summary of this section so that a reader will have a full understanding of what happened.
    Your response should be fully encompass what was said in the passage.

    ```{text}```
    FULL SUMMARY:
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])

    map_chain = load_summarize_chain(
        llm=llm,
        prompt=map_prompt_template
        )
    
    summaries = get_summaries(map_chain, selected_indices, docs)
    return summaries

load_dotenv()
doc = Doc.Document()
doc.load_from_pdf('./Books/Final_proba_(1111.pdf')

cleaned_text = doc.data
docs, vectors = emb.generate_embedding(open_source=False, text=cleaned_text)

llm = ChatGoogleGenerativeAI(model="gemini-pro")

num_clusters = 5
summaries = cluster_and_summarize(num_clusters)
