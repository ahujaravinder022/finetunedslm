'''import streamlit as st
import torch
from transformers import pipeline
import pandas as pd

# Load the text generation pipeline
chatbot = pipeline("text-generation", model="Qwen/Qwen2.5-Coder-7B-Instruct")

st.title("🤖 Qwen Coder 2.5 7B model")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat container (keeps chat messages at top)
chat_container = st.container()
with chat_container:
    # Display previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input (always sticks at bottom in Streamlit)
if prompt := st.chat_input("Ask me anything...Enter your Question here"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.spinner("Thinking..."):
        conversation = chatbot(prompt, max_new_tokens=600)
        response = conversation[0].get("generated_text", "")
        if response is None:
            response = ""  # fallback if None
        if response.startswith(prompt):
            response = response[len(prompt):].strip()

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# -------------------------
# FEEDBACK SECTION AT END
# -------------------------
with st.container():
    st.markdown("---")
    st.subheader("📝 Feedback")

    feedback_text = st.text_area("Please provide your feedback here:")

    excel_file = 'feedback.xlsx'
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['prompt', 'response', 'Feedback', 'Timestamp'])

    if st.button("Submit Feedback"):
        if feedback_text.strip():
            new_feedback = pd.DataFrame([{
                'prompt': st.session_state.messages[-2]["content"] if len(st.session_state.messages) >= 2 else "",
                'response': st.session_state.messages[-1]["content"] if len(st.session_state.messages) >= 1 else "",
                'Feedback': feedback_text,
                'Timestamp': pd.Timestamp.now()
            }])
            df = pd.concat([df, new_feedback], ignore_index=True)
            df.to_excel(excel_file, index=False)
            st.success("✅ Feedback submitted successfully!")
        else:
            st.warning("⚠️ Please enter your feedback before submitting.")

'''


import streamlit as st
import torch
from transformers import pipeline
import pandas as pd

# Load the text generation pipeline
chatbot = pipeline("text-generation", model="Qwen/Qwen2.5-Coder-7B-Instruct")

st.title("🤖 Qwen Coder 2.5 7B model")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything...Enter your prompt here"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.spinner("Thinking..."):
        conversation = chatbot(prompt, max_new_tokens=200)

        # Safely extract generated text
        response = conversation[0].get("generated_text", "")
        if response is None:
            response = ""  # fallback if None

        # Remove the prompt part (optional, cleaner output)
        if response.startswith(prompt):
            response = response[len(prompt):].strip()

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)


sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
selected = st.feedback("thumbs")
if selected is not None:
    st.markdown(f"You selected: {sentiment_mapping[selected]}")

# -------------------------
# FEEDBACK SECTION AT END (Collapsible)
# -------------------------
st.markdown("---")
with st.expander("📝 Leave Feedback"):
    feedback_text = st.text_area("Please provide your feedback here:")

    excel_file = 'feedback.xlsx'
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['prompt', 'response', 'Feedback', 'Timestamp'])

    if st.button("Submit Feedback"):
        if feedback_text.strip():
            new_feedback = pd.DataFrame([{
                'prompt': st.session_state.messages[-2]["content"] if len(st.session_state.messages) >= 2 else "",
                'response': st.session_state.messages[-1]["content"] if len(st.session_state.messages) >= 1 else "",
                'Feedback': feedback_text,
                'Timestamp': pd.Timestamp.now()
            }])
            df = pd.concat([df, new_feedback], ignore_index=True)
            df.to_excel(excel_file, index=False)
            st.success("✅ Feedback submitted successfully!")
        else:
            st.warning("⚠️ Please enter your feedback before submitting.")
