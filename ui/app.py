import streamlit as st
import uuid
from api_client import query_api
from components.sidebar import render_sidebar
from components.chat import render_chat, add_message
from components.utils import show_confidence, show_sources

st.set_page_config(page_title="Enterprise RAG Assistant", layout="wide")

st.title("💬 Enterprise RAG Assistant")

# Sidebar
settings = render_sidebar()

# Session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Chat UI
query = render_chat()

if query:

    add_message("user", query)

    payload = {
        "query": query,
        "tenant_id": settings["tenant_id"],
        "department": settings["department"],
        "source": settings["source"],
        "session_id": st.session_state.session_id
    }

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        for chunk in query_api(payload):
            full_response += chunk
            placeholder.markdown(full_response)

    add_message("assistant", full_response)

    # ⚠️ OPTIONAL: if backend returns JSON instead of stream
    # show_confidence(response["confidence"])
    # show_sources(response["source"])