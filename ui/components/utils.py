import streamlit as st


def show_confidence(confidence):
    if confidence >= 0.7:
        st.success(f"Confidence: {confidence:.2f}")
    elif confidence >= 0.4:
        st.warning(f"Confidence: {confidence:.2f}")
    else:
        st.error(f"Confidence: {confidence:.2f}")


def show_sources(sources):
    if not sources:
        return

    with st.expander("📄 Sources"):
        for i, s in enumerate(sources):
            st.write(f"**Chunk {i+1}:** {s.get('text', '')[:200]}...")