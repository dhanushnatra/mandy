import streamlit as st
from agent import ask_agent

st.set_page_config(page_title="Mandy - Manufacturing Assistant", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Manufacturing AI Agent Mandy. How can I assist you today?"}
    ]

st.title("💬 Chat with Mandy")

# Display conversation history
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])
    else:
        with st.chat_message("user"):
            st.write(msg["content"])



# Chat input
user_input = st.chat_input("Type your message...",)

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # Create AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.write("Thinking...")
        
        response = ask_agent(st.session_state.messages)
    assistant_reply = response

    # Update placeholder
    message_placeholder.write(assistant_reply)

    # Add response to history
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )
