import streamlit as st


def render_sidebar():
    st.sidebar.title("⚙️ Settings")

    tenant_id = st.sidebar.text_input("Tenant ID", "company_a")

    department = st.sidebar.selectbox(
        "Department",
        ["", "HR", "Finance", "Engineering"]
    )

    source = st.sidebar.text_input("Source (optional)")

    return {
        "tenant_id": tenant_id,
        "department": department,
        "source": source
    }