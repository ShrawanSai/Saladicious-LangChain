import streamlit as st
from streamlit_chat import message
from backend.core import run_llm, run_llm_for_chat

st.set_page_config(page_title="Saladicious AI Salad Chef Assistant", page_icon="📈")
st.sidebar.header("Saladicious AI Salad Chef Assistant")
st.title("Saladicious AI Salad Chef Assistant")

prompt = st.chat_input("Ask me anything about salads and I will help you out!")

if "user_prompt_history" not in st.session_state:
    st.session_state.user_prompt_history = []

if "chat_answers_history" not in st.session_state:
    st.session_state.chat_answers_history = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if prompt:
    with st.spinner("Thinking..."):
        result = run_llm_for_chat(prompt,chat_history = st.session_state.chat_history)['answer']

        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answers_history.append(result)
        st.session_state.chat_history.append((prompt, result))


if st.session_state.user_prompt_history:

    for i, (user_prompt, chat_answer) in enumerate(zip(st.session_state.user_prompt_history, st.session_state.chat_answers_history)):
        message(user_prompt, is_user=True)
        message(f"AI Assistant: {chat_answer}")
    st.markdown(
    """
    <script>
    var element = document.getElementById("end-of-chat");
    element.scrollIntoView({behavior: "smooth"});
    </script>
    """,
    unsafe_allow_html=True,
)
       