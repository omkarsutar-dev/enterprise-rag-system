import streamlit as st

from components.sidebar import render_sidebar
from components.uploader import render_uploader
from components.chat import render_chat


st.set_page_config(
    page_title="Enterprise RAG",
    layout="wide"
)

st.title("Enterprise Adaptive RAG System")

tenant_id, department = render_sidebar()

render_uploader(
    tenant_id,
    department
)

render_chat(
    tenant_id,
    department
)