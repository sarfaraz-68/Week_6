import sys
from pathlib import Path

import streamlit as st


sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from rag_pipeline import ask_question


st.set_page_config(
    page_title="Sanitation Document Q&A",
    page_icon="📄"
)

st.title("📄 Sanitation Document Q&A")

st.write(
    "Ask a question and get an answer based only on the provided sanitation document."
)

question = st.text_input(
    "Ask your question:",
    placeholder="Example: What are the health benefits of safe sanitation?"
)

if st.button("Ask Question"):
    if question:
        with st.spinner("Searching the document and generating an answer..."):
            answer = ask_question(question)

        st.subheader("Answer")
        st.write(answer)

    else:
        st.warning("Please enter a question first.")