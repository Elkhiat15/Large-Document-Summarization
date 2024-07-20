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
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2),
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
    
    return conversation_chain.run(input_question)
