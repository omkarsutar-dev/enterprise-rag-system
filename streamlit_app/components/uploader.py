import streamlit as st

from api_client import upload_document


def render_uploader(tenant_id, department):

    st.subheader("Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a file"
    )

    if uploaded_file:

        if st.button("Upload"):

            response = upload_document(
                uploaded_file,
                tenant_id,
                department
            )

            st.success(response["message"])