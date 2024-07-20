from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain.agents import AgentType, load_tools, initialize_agent, Tool
from dotenv import load_dotenv
from summerize import summarize  # Ensure this is a callable function
load_dotenv()

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

def get_agent(vector_store, temperature=0.2, n_clusters=5):
    '''
        Loads the necessary tools for the agent.
        
            Parameters:
                vector_store (VectorStore): The vector store to use for conversation.
                temperature (float): The temperature to use for conversation messages (0 to 1)
                n_clusters (int): Number of clusters for summarization.

            Returns:
                agent (AgentExecutor): An agent that can be used to interact with different tools.
    '''

    retrieval_qa = get_conversation_chain(vector_store=vector_store, temperature=temperature)
    
    # Ensure summarize_chain is a callable function
    summarize_chain = lambda text: summarize(text, n_clusters=n_clusters)

    tools = [
        Tool(
            name="Retrieval QA System",
            func=retrieval_qa.run,
            description="Useful for answering questions."
        ),
        Tool(
            name='Summarizer',
            func=summarize_chain,
            description='Useful for summarizing texts'
        )
    ]

    # Load additional tools
    additional_tools = load_tools(["math-llm", "serpapi"], llm=GoogleGenerativeAI(model="gemini-1.5-flash",temperature=temperature))
    tools.extend(additional_tools)

    agent = initialize_agent(
        tools=tools,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    return agent

def run_agent(input_question, vector_store, temperature=0.2, n_clusters=5):
    '''
        Runs the agent to answer questions given an input question.
        
            Parameters:
                input_question (str): The question to be answered.
                vector_store (VectorStore): The vector store to use for conversation.
                temperature (float): The temperature to use for conversation messages (0 to 1)
                n_clusters (int): Number of clusters for summarization.

            Returns:
                answer (str): The answer to the input question.
    '''

    agent = get_agent(vector_store=vector_store, temperature=temperature, n_clusters=n_clusters)
    response = agent.run(input_question)
    print(response)

# Example usage:
# vector_store = YourVectorStoreImplementation()
# input_question = "What does this book talk about?"
# run_agent(input_question=input_question, vector_store=vector_store)
