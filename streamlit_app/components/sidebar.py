import streamlit as st


def render_sidebar():

    st.sidebar.title("Enterprise RAG")

    tenant_id = st.sidebar.text_input(
        "Tenant ID",
        value="company_a"
    )

    department = st.sidebar.text_input(
        "Department",
        value=""
    )

    return tenant_id, department