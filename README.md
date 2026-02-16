# PDF RAG Reader 📄

An AI-powered PDF question-answering application using Retrieval Augmented Generation (RAG).

## Features

- 📤 Upload PDF documents
- 💬 Chat with your PDFs using natural language
- 🤖 Powered by Hugging Face models (Qwen/Qwen2.5-72B-Instruct)
- 🔍 Local embeddings for fast retrieval (sentence-transformers)
- 🎨 Modern chat interface with Streamlit

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd PDF_reader
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file:
```
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here
```

4. **Run the app**
```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and branch
5. Set main file path to `app.py`
6. Add your `HUGGINGFACEHUB_API_TOKEN` in Secrets:
   ```toml
   HUGGINGFACEHUB_API_TOKEN = "your_token_here"
   ```
7. Click "Deploy"!

## Architecture

- **Frontend**: Streamlit (chat interface)
- **Backend**: LangChain + ChromaDB (vector storage)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (local)
- **LLM**: Qwen/Qwen2.5-72B-Instruct via Hugging Face Inference API

## Usage

1. Upload a PDF using the sidebar
2. Wait for processing (this creates embeddings)
3. Ask questions in the chat!
4. Get AI-powered answers based on your document

## License

MIT
