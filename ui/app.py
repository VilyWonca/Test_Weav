import os

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

from ollama import chat
import streamlit as st

st.title("S_MAKE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Как дела?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = chat(
            model='owl/t-lite:latest',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )
        response = st.write_stream(i['message']['content'] for i in stream)
    st.session_state.messages.append({"role": "assistant", "content": response})