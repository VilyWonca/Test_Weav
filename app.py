from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
from services.prompt_builder import PromptBuild
from services.wv_search import WeaviateSearcher

load_dotenv()

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

prompt_builder = PromptBuild()
searcher_wv = WeaviateSearcher()

st.title("S_MAKE")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

search_type = st.selectbox(
    "🔍 Выберите тип поиска:",
    ["По ключевым словам", "По вектору (семантический)", "Гибридный поиск"]
) 

print("Вот такой тип поиска выбрал пользователь:", search_type)

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
        chunks_dict = searcher_wv.search(prompt, 10, "Books", search_type)

        print("Строим промпт...")
        context_chunk = prompt_builder.build_prompt(chunks_dict, prompt)[1]
        context_prompt = prompt_builder.build_prompt(chunks_dict, prompt)[0]
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

        st.markdown("**Ответ от нейросети:**")
        response = st.write_stream(extract_text_from_stream(stream))
        with st.expander("**Отрывки текста, которые использовались при ответе:**"):
            st.markdown(
            f"""
            <div style= "background-color:#1A1C23; padding: 25px; border-radius: 16px;">{context_chunk}</div>
            """,
            unsafe_allow_html=True
            )

