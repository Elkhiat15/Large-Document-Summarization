import numpy as np

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.chains.llm import LLMChain
from langchain.chains.summarize import load_summarize_chain
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from dotenv import load_dotenv


def get_indices(num_clusters, kmeans, vectors):
    '''
        Gets the closest indices to clusters centriods to be summarized.
        
            Parameters:
                num_clusters (int): Number of clusters.
                kmeans (KMeans): A fitted K-Means model.
                vectors (list[list[float]]): A list of embeddings for the input text chunks.

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


def get_best_model(vectors):
    '''
        Gets the best number of clusters using Silhouette score method.
        
            Parameters:
                vectors (list[list[float]]): A list of embeddings for the input text chunks.

            Returns:
                best_model (KMeans): The best model fitted to vectors usnig best number of clusters.
                best_k (int): The best number of clusters using Silhouette score method.
    '''        
    
    max_k = min(len(vectors), 20)
    scores = [silhouette_score(vectors, KMeans(n_clusters=k, n_init=1).fit_predict(vectors)) for k in range(2, max_k)]
    best_k = np.argmax(scores) + 2
    best_model = KMeans(n_clusters=best_k, n_init=1).fit(vectors)
   
    return best_model, best_k


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


def cluster_and_summarize(docs, vectors):
    '''
        Gets the summary of each selected chunk after clustring then combines the summaries into one document.
        
            Parameters:
                docs (list[Document]): A list of documents where each document holds a chunck of the whole document.
                vectors (list[list[float]]): A list of embeddings for the input text chunks.
                
            Returns:
                summaries (Document): The combined summaries.
    '''        
    best_model, best_n_clusters = get_best_model(vectors)
    
    selected_indices = get_indices(best_n_clusters, best_model, vectors)

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


def summarize(docs ,vectors, guide="", summaries = None):
    '''
        Gets the summary of all summaries and refined the summary using user guide if any.
        
            Parameters:
                docs (list[Document]): A list of documents where each document holds a chunck of the whole document.
                vectors (list[list[float]]): A list of embeddings for the input text chunks.
                guide (str): A guide (rule) from user to refine the summary
                summaries (Document): The combined summaries.
                
            Returns:
                summaries (Document): The combined summaries.
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
    if guide!="":
        guide_prompt = f"Consider the user guide when summarizing guide: ({guide})"
        combine_prompt = guide_prompt+"\n"+ combine_prompt  
    
    if summaries == None:
        summaries = cluster_and_summarize(docs, vectors)
    
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

    reduce_chain = load_summarize_chain(
        llm=llm,
        prompt=combine_prompt_template
        )

    output = reduce_chain.invoke([summaries])
    full_summary = output['output_text']
    return summaries, full_summary  


def refine_summary(prev_summary):
    '''
        Automatically refines the response for EX: using more simple sentenses remove unneeded words etc...
        
            Parameters:
                prev_summary (str): The previous summary provided by the model.

            Returns:
                refined_summary (str): The Refined summary.
    '''        

    refine_prompt = """
    You will be given a summary which you provided to the reader earlier saying {text}
    Your goal is to refine this summary to a better one.
    The refined summary you give the reader should be coherance and easy to grasp.
    Your output should be as long as the summary provided to you and should be devidid into parts.
    """
    refine_prompt_template = PromptTemplate(template=refine_prompt, input_variables=["text"])

    refine_chain = LLMChain(
        llm=llm,
        prompt=refine_prompt_template
        )
    
    refined_summary = refine_chain.predict(text= prev_summary)
    
    return refined_summary


def get_cumulative_summary(docs, vectors, prev_summary):
    '''
        Summarizes the given documents then combined it with the previous summary and finnaly summarize the two summaries.
        
            Parameters:
                docs (list[Document]): A list of documents where each document holds a chunck of the whole document.
                vectors (list[list[float]]): A list of embeddings for the input text chunks.
                prev_summary (str): The previous summary provided by the model 
                                    after summarizing the given documents at the start of program.

            Returns:
                cumulative_summary (str): The summary provided by the model after summarize.
    '''        

    cumulative_prompt = """
    You will be given two summaries each is a summary from a one book or many books.
    The summaries will be enclosed in triple backticks (```)
    Your goal is to Combine the two summaries into one summary.
    The combined summary you give the reader should be coherance and divided into parts like the two summary.
    

    ```{text}```
    COMBINED SUMMARY:
    """
    _ , summary = summarize(docs, vectors)
    cumulative_prompt_template = PromptTemplate(template=cumulative_prompt, input_variables=["text"])

    reduce_chain = load_summarize_chain(
        llm=llm,
        prompt=cumulative_prompt_template
        )
    
    two_summaries = summary+"\n"+ prev_summary
    two_summaries = Document(page_content=two_summaries)
    output = reduce_chain.invoke([two_summaries])
    cumulative_summary = output['output_text']
    return cumulative_summary  


# intializing the LLModel
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-pro")