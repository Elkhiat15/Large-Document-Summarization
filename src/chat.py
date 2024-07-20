from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI


def get_conversation_chain(vector_store):
    '''
        Creates a conversation chain using the provided vector store.
        
            Parameters:
                vector_store (VectorStore): The vector store to use for conversation.

            Returns:
                chain (Chain): A chain that can be used to interact with the vector store.
    '''
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=2),
        memory=memory,
        retriever=vector_store.as_retriever()  
    )

    return conversation_chain
    