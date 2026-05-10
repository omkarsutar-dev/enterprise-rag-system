import streamlit as st
import requests
import json

from api_client import query_rag


def render_chat(tenant_id, department):

    st.subheader("Chat")

    # ✅ Session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # =========================
    # ✅ Render Chat History
    # =========================
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            # 👤 USER
            if msg["role"] == "user":

                st.markdown(msg["content"])

            # 🤖 ASSISTANT
            else:

                st.markdown(msg["answer"])

                confidence = msg.get("confidence", 0)

                # ✅ Confidence Badge
                if confidence >= 0.7:
                    st.success(f"Confidence: {confidence:.2f}")

                elif confidence >= 0.4:
                    st.warning(f"Confidence: {confidence:.2f}")

                else:
                    st.error(f"Confidence: {confidence:.2f}")

                # ✅ Sources
                sources = msg.get("sources", [])

                if sources:

                    with st.expander("Sources"):

                        for idx, source in enumerate(sources, start=1):

                            heading = source.get("heading", "Unknown")

                            text = source.get("text", "")

                            score = source.get("final_score", 0)

                            st.markdown(
                                f"""
                                ### Source {idx}
                                **Heading:** {heading}

                                **Score:** {score:.2f}

                                **Content:**
                                {text}
                                """
                            )

    # =========================
    # ✅ Chat Input
    # =========================
    query = st.chat_input("Ask a question")

    if query:

        # ✅ Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        # ✅ Render user immediately
        with st.chat_message("user"):
            st.markdown(query)

        payload = {
            "query": query,
            "tenant_id": tenant_id,
            "department": department,
            "source": "",
            "session_id": "streamlit_session"
        }

        try:

            # ✅ API Call
            response = requests.post(
                "http://127.0.0.1:8000/query",
                json=payload,
                stream=True
            )

            full_response = ""

            # =========================
            # ✅ Streaming Assistant UI
            # =========================
            with st.chat_message("assistant"):

                placeholder = st.empty()

                for chunk in response.iter_content(
                    chunk_size=1024,
                    decode_unicode=True
                ):

                    if chunk:

                        full_response += chunk

                        placeholder.markdown("Generating response...")

                # ✅ Parse JSON response
                data = json.loads(full_response)

                answer = data.get(
                    "answer",
                    "No answer generated."
                )

                confidence = data.get(
                    "confidence",
                    0
                )

                sources = data.get(
                    "source",
                    []
                )

                # ✅ Final answer
                placeholder.markdown(answer)

                # ✅ Confidence Badge
                if confidence >= 0.7:
                    st.success(f"Confidence: {confidence:.2f}")

                elif confidence >= 0.4:
                    st.warning(f"Confidence: {confidence:.2f}")

                else:
                    st.error(f"Confidence: {confidence:.2f}")

                # ✅ Sources Viewer
                if sources:

                    with st.expander("Sources"):

                        for idx, source in enumerate(sources, start=1):

                            heading = source.get("heading", "Unknown")

                            text = source.get("text", "")

                            score = source.get("final_score", 0)

                            st.markdown(
                                f"""
                                ### Source {idx}
                                **Heading:** {heading}

                                **Score:** {score:.2f}

                                **Content:**
                                {text}
                                """
                            )

            # ✅ Save assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "answer": answer,
                "confidence": confidence,
                "sources": sources
            })

        except Exception as e:

            st.error(f"Error: {str(e)}")