import streamlit as st
import openai

# UI Header
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot using OpenAI's GPT-3.5 model. "
    "Enter your API key to get started. Get it [here](https://platform.openai.com/account/api-keys)."
)

# API Key Input
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    openai.api_key = openai_api_key

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Placeholder for assistant's message
        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            stream = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            for chunk in stream:
                if "choices" in chunk and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta.get("content", "")
                    full_response += delta
                    response_container.markdown(full_response + "▌")
            response_container.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
