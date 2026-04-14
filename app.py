import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# -----------------------------
# Initialize Groq client
# -----------------------------
client = Groq(api_key=api_key)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Groq Chatbot", page_icon="💬")

st.title("💬 AI Chatbot using Groq")
st.write("Ask anything!")

# -----------------------------
# Session state for chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful, polite, and professional AI assistant."
        }
    ]

# -----------------------------
# Display chat history
# -----------------------------
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# -----------------------------
# User input
# -----------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Display user message
    st.chat_message("user").write(user_input)

    try:
        # API call
        response = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama-3.1-8b-instant"
        )

        bot_reply = response.choices[0].message.content

    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    # Add bot response
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

    # Display bot response
    st.chat_message("assistant").write(bot_reply)

# -----------------------------
# Clear chat button
# -----------------------------
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]
    st.rerun()