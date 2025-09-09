import streamlit as st
import torch
from transformers import pipeline
 # Load the conversational pipeline
    # Replace 'facebook/blenderbot-400M-distill' with your chosen model

#chatbot = pipeline("question-answering", model="facebook/blenderbot-400M-distill")
chatbot = pipeline("text-generation", model="Qwen/Qwen2.5-Coder-7B-Instruct")


st.title("Hugging Face Chatbot")

    # Initialize chat history
if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
with st.spinner("Thinking..."):
            # Prepare conversation object for the chatbot
            # You might need to adapt this based on the model's expected input format
            conversation = chatbot(prompt)
            response = conversation["generated_text"]

        # Add bot response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})
with st.chat_message("assistant"):
            st.markdown(response)
