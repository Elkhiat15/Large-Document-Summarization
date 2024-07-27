from css_styles import css, bot_template, user_template

def run(st, chain, question_anwering):
    st.markdown(css, unsafe_allow_html=True)
    
    st.header("Welcome to QA Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    _,c,_ = st.columns(spec=[1,5,1])
    c.subheader(":blue[Enter your question]")
    user_question = c.text_input("Enter your question:", label_visibility="collapsed")
    if user_question!="":
        # Get the answer to the user's question
        with st.spinner("Thinking 💡"):
            answer = question_anwering(user_question, chain)
        # Update the chat history
        st.session_state.chat_history.append(("User", user_question))
        st.session_state.chat_history.append(("Bot", answer))

        with st.container(border=True, height=700):    
            for speaker, message in st.session_state.chat_history:
                if speaker == "User":
                    st.write(user_template.replace("{{MSG}}", message),
                        unsafe_allow_html=True)
                else:
                    st.write(bot_template.replace("{{MSG}}", f"\n\n{message}\n\n"),
                            unsafe_allow_html=True)
  
    else:
        st.session_state.chat_history = []
    