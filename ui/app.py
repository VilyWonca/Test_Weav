import os

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

from ollama import chat
import streamlit as st

st.title("S_MAKE")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")