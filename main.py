from collections.abc import Generator

import ollama
import streamlit as st


def ollama_generator(model_name: str, messages: dict) -> Generator:
    stream = ollama.chat(model=model_name, messages=messages, stream=True)
    for chunk in stream:
        yield chunk["message"]["content"]


st.title(body="Ollama Chat :speech_balloon:")

if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""

if "available_models" not in st.session_state:
    st.session_state.available_models = [model.model for model in ollama.list().models]

if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.selected_model = st.selectbox(
    label="Please select the model:",
    options=st.session_state.available_models,
)

for message in st.session_state.messages:
    with st.chat_message(name=message["role"]):
        st.markdown(body=message["content"])

if prompt := st.chat_input(placeholder="How could I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message(name="user"):
        st.markdown(body=prompt)

    with st.chat_message(name="assistant"):
        response = st.write_stream(
            stream=ollama_generator(
                model_name=st.session_state.selected_model,
                messages=st.session_state.messages,
            )
        )

    st.session_state.messages.append({"role": "assistant", "content": response})
