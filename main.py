
import streamlit as st
from agent import ask_agent

st.set_page_config(page_title="Mandy", page_icon="💬")

if "messages" not in st.session_state:
    st.session_state.messages = []

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

def get_assistant_response():
    return ask_agent(st.session_state.messages[-1]["content"]) if st.session_state.messages else ""

if st.button("Clear Conversation"):
    st.session_state.messages = []

st.title("Mandy 💬 Manufacturing Intelligence Agent ")

# Display messages
use_chat_message = hasattr(st, "chat_message")
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if use_chat_message:
        with st.chat_message(role):
            st.markdown(content)
    else:
        if role == "user":
            st.markdown(f"**You:** {content}")
        elif role == "assistant":
            st.markdown(f"**Assistant:** {content}")
        else:
            st.markdown(f"**{role.capitalize()}:** {content}")

# Input form
with st.form("input_form", clear_on_submit=True):
    user_input = st.text_input("Message", "")
    submitted = st.form_submit_button("Send")
    if submitted and user_input.strip()!="":
        add_message("user", user_input)
        # show the user's message immediately in UI
        if use_chat_message:
            with st.chat_message("user"):
                st.markdown(user_input)
            with st.chat_message("assistant"):
                placeholder = st.empty()
                placeholder.markdown("...")
        # Get assistant reply
        reply = get_assistant_response()
        add_message("assistant", reply)

        # If we used placeholder, replace it
        if use_chat_message:
            placeholder.markdown(reply)
        