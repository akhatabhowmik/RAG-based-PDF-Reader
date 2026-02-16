from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

def main():
    # 1. Load Documents
    print("Loading PDFs...")
    loader = PyPDFDirectoryLoader(DATA_PATH)
    raw_documents = loader.load()
    
    if not raw_documents:
        print("No PDFs found in data directory.")
        return

    # 2. Split Text
    print("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(raw_documents)
    print(f"Split into {len(chunks)} chunks.")

    # 3. Create Vector Store
    # Using local embeddings - free and private!
    print("Initializing embeddings (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Clean up old DB if it exists to avoid conflicts
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    print("Creating vector database...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="growing_vegetables"
    )
    
    print("Database populated successfully.")

if __name__ == "__main__":
    main()