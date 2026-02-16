import streamlit as st
import os
from pathlib import Path
import rag_engine

# Page config
st.set_page_config(
    page_title="PDF RAG Reader",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">📄 PDF RAG Reader</p>', unsafe_allow_html=True)
st.markdown("Upload a PDF and ask questions about its content using AI-powered retrieval.")

# Sidebar for PDF upload
with st.sidebar:
    st.header("📁 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file is not None:
        # Save uploaded file
        upload_dir = Path("data")
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir / uploaded_file.name
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process the PDF
        with st.spinner("Processing PDF..."):
            try:
                success = rag_engine.process_pdf(str(file_path))
                if success:
                    st.success(f"✅ Successfully processed: {uploaded_file.name}")
                    st.session_state['pdf_processed'] = True
                    st.session_state['current_pdf'] = uploaded_file.name
                else:
                    st.error("Failed to process PDF")
                    st.session_state['pdf_processed'] = False
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
                st.session_state['pdf_processed'] = False
    
    # Show current PDF status
    if 'current_pdf' in st.session_state:
        st.info(f"📄 Current PDF: {st.session_state['current_pdf']}")
    
    st.divider()
    st.caption("Powered by Hugging Face 🤗")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your PDF..."):
    # Check if PDF is uploaded
    if not st.session_state.get('pdf_processed', False):
        st.warning("⚠️ Please upload a PDF first!")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = rag_engine.get_answer(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Add a clear chat button in sidebar
with st.sidebar:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
