from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.agents import AgentType,load_tools,initialize_agent,Tool
# from dotenv import load_dotenv
# from summerize import summarize
# from langchain_google_genai import GoogleGenerativeAI
# load_dotenv()


# def get_agent(vector_store, temperature=0.2, n_clusters=5):
#     '''
#         Loads the necessary tools for the agent.
        
#             Returns:
#                 tools (List[Tool]): A list of tools that can be used by the agent.
#     '''
#     search = GoogleSearchAPIWrapperCopy()

#     retrieval_qa = get_conversation_chain(vector_store=vector_store,
#                                           temperature=temperature)
    
#     summarize_chain = summarize(n_clusters=n_clusters)

#     tools = [
#         Tool(
#             name="Search",
#             func=search.run,
#             description="useful of finding information about recent events"
    
#         ),

#         Tool(
#             name="Retrieval QA System",
#             func=retrieval_qa.run,
#             description="Useful for answering questions."
#         ),

#         Tool(
#             name='Summarizer',
#             func=summarize_chain,
#             description='useful for summarizing texts'

#         ),
        
#     ]

#     math_tool = load_tools(["math-llm"], llm = GoogleGenerativeAI(, temperature=temperature))[0]
#     tools.append(math_tool)

#     agent = initialize_agent(
#         tools=tools,
#         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         verbose=True,

#     )

#     return agent


def get_conversation_chain(vector_store, temperature):
    '''
        Creates a conversation chain using the provided vector store.
        
            Parameters:
                vector_store (VectorStore): The vector store to use for conversation.
                temperature (float): The temperature to use for conversation messages (0 to 1)
            Returns:
                chain (Chain): A chain that can be used to interact with the vector store.
    '''
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temperature),
        memory=memory,
        retriever=vector_store.VectorStore.as_retriever()  
    )

    return conversation_chain



def question_anwering(input_question, conversation_chain, return_context=False):
    '''
        Uses the conversation chain to answer questions given an input question.
        
            Parameters:
                input_question (str): The question to be answered.
                conversation_chain (Chain): The conversation chain to use for answering questions.
                return_context (bool): Flag to determine whether to return the context along with the answer.

            Returns:
                answer (str): The answer to the input question.
                context (str): The context that led to the answer, if `return_context` is True.
    '''
    
    if return_context:
        return conversation_chain.invoke(input_question)
    
    return conversation_chain.invoke(input_question)["answer"]


# def run_agent(input_question, vector_store, temperature=0.2, n_clusters=5):
#     '''
#         Runs the agent to answer questions given an input question.
        
#             Parameters:
#                 input_question (str): The question to be answered.
#                 vector_store (VectorStore): The vector store to use for conversation.
#                 temperature (float): The temperature to use for conversation messages (0 to 1)
#                 n_clusters (int): Number of clusters for summarization.

#             Returns:
#                 answer (str): The answer to the input question.
#     '''

#     agent = get_agent(vector_store=vector_store, temperature=temperature, n_clusters=n_clusters)
#     print(agent.run(input_question))


    