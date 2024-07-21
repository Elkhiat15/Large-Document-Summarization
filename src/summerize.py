#import Doc, Embedding as emb
import numpy as np

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.chains.summarize import load_summarize_chain
from sklearn.cluster import KMeans
from dotenv import load_dotenv

def get_indices(num_clusters, kmeans, vectors):
    '''
        Gets the closest indices to clusters centriods to be summarized.
        
            Parameters:
                num_clusters (int): Number of clusters.
                kmeans (KMeans): A fitted K-Means model.
        
            Returns:
                selected_indices (list[int]): A list of indices of data points closest to each centriod.
    '''        

    closest_indices = []

    for i in range(num_clusters):
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append(closest_index)
        selected_indices = sorted(closest_indices)
    
    return selected_indices

def get_summaries(map_chain, selected_indices, docs):
    '''
        Gets the summary of each selected chunk after clustring then combines the summaries into one document.
        
            Parameters:
                map_chain (BaseCombineDocumentsChain): A langchain LLM the is responsible for summarize chunks.
                selected_indices (list[int]): A list of indices of data points closest to each centriod.
                docs (list[Document]): A list of documents where each document holds a chunck of the whole document.

            Returns:
                summaries (Document): The combined summaries.
    '''        

    selected_docs = [docs[idx] for idx in selected_indices]

    summary_list = []
    for i, doc in enumerate(selected_docs):
        chunk_summary = map_chain.invoke([doc])
        summary_list.append(chunk_summary['output_text'])

    summaries = "\n".join(summary_list)
    summaries = Document(page_content=summaries)
    return summaries

def cluster_and_summarize(num_clusters, docs, vectors):
    '''
        Gets the summary of each selected chunk after clustring then combines the summaries into one document.
        
            Parameters:
                num_clusters (int): Number of clusters.
                
            Returns:
                summaries (Document): The combined summaries.
    '''        

    kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(vectors)

    selected_indices = get_indices(num_clusters, kmeans, vectors)

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

#def summarize_all(summaries):
    '''
        Gets the summary of all summaries.
        
            Parameters:
                summaries (Document): The combined summaries.
                
            Returns:
                full_summary (str): The full summary we target.
    '''        

    combine_prompt = """
    You will be given a series of summaries from a one book or many books. The summaries will be enclosed in triple backticks (```)
    Your goal is to give a verbose summary of what said in those summaries.
    The finall summary you give the reader should be coherance and easy to grasp the whole summaries.
    You should consider the order of summaries and divide the summary to parts.

    ```{text}```
    VERBOSE SUMMARY:
    """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

    reduce_chain = load_summarize_chain(
        llm=llm,
        prompt=combine_prompt_template
        )

    output = reduce_chain.invoke([summaries])
    full_summary = output['output_text']
    return full_summary  


####################################### Suggested Modification ##############################
def summarize(n_clusters, docs ,vectors):
    '''
        Gets the summary of all summaries.
        
            Parameters:
                summaries (Document): The combined summaries.
                
            Returns:
                full_summary (str): The full summary we target.
    '''        

    combine_prompt = """
    You will be given a series of summaries from a one book or many books. The summaries will be enclosed in triple backticks (```)
    Your goal is to give a verbose summary of what said in those summaries.
    The finall summary you give the reader should be coherance and easy to grasp the whole summaries.
    You should consider the order of summaries and divide the summary to parts.

    ```{text}```
    VERBOSE SUMMARY:
    """
    summaries = cluster_and_summarize(n_clusters,docs, vectors)
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

    reduce_chain = load_summarize_chain(
        llm=llm,
        prompt=combine_prompt_template
        )

    output = reduce_chain.invoke([summaries])
    full_summary = output['output_text']
    return full_summary  
#########################################################################


# intializing the LLModel
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-pro")

# # loading, cleaning and embedding
# doc = Doc.Document()
# doc.load_from_pdf('./Books/Final_proba_(1111.pdf')
# cleaned_text = doc.data
# docs, vectors = emb.generate_embedding(open_source=False, text=cleaned_text)

# # summarizing
# num_clusters = 5
# summaries = cluster_and_summarize(num_clusters)
# response = summarize_all(summaries)

# print(f"\033[1;32m {response} \033[0m") # to print in green in terminal 
