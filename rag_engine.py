import os
from typing import List
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from huggingface_hub import InferenceClient

load_dotenv()

# Global variable to store the vectorstore instance
vectorstore = None

def process_pdf(file_path: str):
    """
    Loads a PDF, splits it into chunks, and creates a vector store.
    """
    global vectorstore

    if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
         print("Error: HUGGINGFACEHUB_API_TOKEN not found in environment.")
         # Token is required for Inference API

    # 1. Load the PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 2. Split the text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)

    # 3. Create Vector Store with Local Embeddings
    print("Generating embeddings locally...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        # persist_directory="./chroma_db" 
    )

    return True

def get_answer(query: str) -> str:
    """
    Answers a query using the initialized RAG pipeline.
    """
    global vectorstore

    if not vectorstore:
        return "Please upload a PDF document first."

    try:
        # 1. Retrieve Context
        retriever = vectorstore.as_retriever()
        retrieved_docs = retriever.invoke(query)
        context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

        # 2. Generate Answer via OpenAI-compatible API
        repo_id = "Qwen/Qwen2.5-72B-Instruct"
        # Using the new OpenAI-compatible endpoint
        api_url = "https://router.huggingface.co/v1/chat/completions"
        # Note: If this fails, we might need to check if the path is just /v1/chat/completions
        
        headers = {
            "Authorization": f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}",
            "Content-Type": "application/json"
        }

        # Prepare Prompt/Messages
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion:\n{query}"}
        ]

        import requests
        response = requests.post(
            api_url,
            headers=headers,
            json={
                "model": repo_id,
                "messages": messages,
                "max_tokens": 2000,
                "temperature": 0.1,
                "stream": False
            }
        )
        
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
            
        return response.json()['choices'][0]['message']['content']

    except Exception as e:
        import traceback
        with open("rag_error.log", "w") as f:
             f.write(f"Error: {str(e)}\n\n")
             traceback.print_exc(file=f)
        return f"Error: {str(e)}"
