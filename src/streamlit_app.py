"""Streamlit chat UI for the RAG Document QA backend."""
import requests
import streamlit as st

API_URL = st.sidebar.text_input("API URL", "http://localhost:8000")

st.title("RAG Document QA")
st.markdown("Upload documents and ask questions about them.")

uploaded_files = st.file_uploader(
    "Upload documents",
    type=["txt", "md", "pdf"],
    accept_multiple_files=True,
)

if uploaded_files and st.button("Ingest"):
    files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
    with st.spinner("Ingesting documents..."):
        response = requests.post(f"{API_URL}/upload", files=files)
    if response.status_code == 200:
        st.success(f"Ingested {response.json().get('ingested', 0)} chunks")
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

st.divider()

question = st.text_input("Ask a question")
if question and st.button("Ask"):
    with st.spinner("Thinking..."):
        response = requests.post(f"{API_URL}/query", json={"question": question})
    if response.status_code == 200:
        data = response.json()
        st.markdown("### Answer")
        st.write(data.get("answer"))
        with st.expander("Sources"):
            st.write(data.get("sources", []))
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
