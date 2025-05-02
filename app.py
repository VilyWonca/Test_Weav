import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
from services.prompt_builder import PromptBuild
from services.wv_search import WeaviateSearcher

prompt_builder = PromptBuild()
searcher_wv = WeaviateSearcher()

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

st.title("S_MAKE")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        print("Извлекаем чанки...")
        chunks = searcher_wv.search(prompt, 2, "Books")
        print("ВОТ ЧАНКИ", chunks)
        print("А ВОТ КАКОГО ОНИ ТИПА", type(chunks), type(chunks[0]))
        print("Строим в промпт...")
        context_prompt = prompt_builder.build_prompt(chunks, prompt)
        print("Вот конечный промпт:", context_prompt)
        print("Передаем в модель...")
        st.session_state.messages.append({"role": "user", "content": context_prompt})
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": prompt}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
