import streamlit as st

def run(stt, chain, get_answer):
    st.markdown("""
        <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
        }
        .chat-bubble {
            padding: 10px 20px;
            border-radius: 10px;
            margin: 10px 0;
            max-width: 80%;
        }
        .user-bubble {
            background-color: #DCF8C6;
            align-self: flex-end;
            margin-left: auto;
        }
        .bot-bubble {
            background-color: #E2E2E2;
            align-self: flex-start;
        }
        .chat-box {
            display: flex;
            flex-direction: column;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    st.header("Welcome to QA Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Enter your question:")
    
    if st.button("Send"):
        if user_question:
            # Get the answer to the user's question
            answer = get_answer(user_question, chain)
            # Update the chat history
            st.session_state.chat_history.append(("User", user_question))
            st.session_state.chat_history.append(("Bot", answer))
    
    # Display the chat history
    chat_html = "<div class='chat-box'>"
    for speaker, message in st.session_state.chat_history:
        if speaker == "User":
            chat_html += f"<div class='chat-bubble user-bubble'><b>{speaker}:</b> {message}</div>"
        else:
            chat_html += f"<div class='chat-bubble bot-bubble'><b>{speaker}:</b> {message}</div>"
    chat_html += "</div>"
    
    st.markdown(chat_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


