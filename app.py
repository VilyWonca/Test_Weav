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
        chunks_dict = searcher_wv.search(prompt, 10, "Books")

        print("Строим промпт...")
        context_prompt = prompt_builder.build_prompt(chunks_dict, prompt)
        print("Вот конечный промпт:", context_prompt)

        # Добавляем настоящий пользовательский запрос
        st.session_state.messages.append({"role": "user", "content": prompt})

        print("Передаем в модель...")
        stream = client.responses.create(
            model=st.session_state["openai_model"],
            input=[
                {"role": m["role"], "content": context_prompt}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        def extract_text_from_stream(stream):
            for chunk in stream:
                if chunk.__class__.__name__ == "ResponseTextDeltaEvent":
                    yield chunk.delta

        # Выводим ответ и сохраняем его
        response = st.write_stream(extract_text_from_stream(stream))
        print("Вот сам ответ от ллм", response)

    st.session_state.messages.append({"role": "assistant", "content": response})
