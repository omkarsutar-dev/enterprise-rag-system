import streamlit as st


def render_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    query = st.chat_input("Ask your question...")

    return query


def add_message(role, content):
    st.session_state.messages.append({
        "role": role,
        "content": content
    })