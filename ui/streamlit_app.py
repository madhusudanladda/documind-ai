import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="DocuMind AI", layout="wide")
st.title("📄 DocuMind AI")
st.caption("Document Intelligence & Grounded Question Answering")

# Sidebar for PDF Upload
with st.sidebar:
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF report", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Process Document", type="primary"):
            with st.spinner("Extracting, chunking and indexing vectors..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    res = requests.post(f"{BACKEND_URL}/upload", files=files)
                    if res.status_code == 200:
                        data = res.json()
                        st.success(f"Indexed {data['pages_extracted']} pages ({data['chunks_created']} chunks)!")
                        st.session_state["doc_loaded"] = True
                    else:
                        st.error(f"Error: {res.json().get('detail', 'Upload failed')}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")

# Main Chat Area
st.subheader("Ask questions about the document")

query = st.text_input("Enter your question:")
top_k = st.slider("Top chunks to retrieve:", min_value=1, max_value=5, value=3)

if st.button("Submit Question") and query:
    with st.spinner("Searching and generating grounded answer..."):
        try:
            res = requests.post(
                f"{BACKEND_URL}/ask",
                json={"question": query, "top_k": top_k}
            )
            if res.status_code == 200:
                result = res.json()
                st.markdown("### Answer")
                st.write(result["answer"])
                
                if result.get("sources"):
                    st.markdown("---")
                    st.markdown("**Sources / Citations:**")
                    cols = st.columns(len(result["sources"]))
                    for i, src in enumerate(result["sources"]):
                        cols[i].info(f"📌 {src}")
            else:
                st.warning(res.json().get("detail", "Error fetching answer"))
        except Exception as e:
            st.error(f"Backend connection error: {e}")