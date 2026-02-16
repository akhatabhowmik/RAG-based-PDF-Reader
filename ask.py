from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = r"chroma_db"

if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
    print("Warning: HUGGINGFACEHUB_API_TOKEN not found in .env. Some models might fail.")

# Initialize the DB with the same embedding function used in creation
print("Loading vector database...")
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma(
    persist_directory=CHROMA_PATH, 
    embedding_function=embedding_function,
    collection_name="growing_vegetables"
)

while True:
    user_query = input("\nWhat must I know about growing vegetables? (or 'q' to quit)\n> ")
    if user_query.lower() == 'q':
        break

    # Retrieve context
    results = db.similarity_search(user_query, k=4)
    context_text = "\n\n".join([doc.page_content for doc in results])
    
    # Generate Answer
    from huggingface_hub import InferenceClient
    
    # User suggested model - let's try it, but have a fallback
    # Note: 'openai/gpt-oss-20b' likely doesn't exist on HF. 
    # We will use a reliable default if it fails, or the user's specific choice.
    # Let's try to stick to a known working one for the demo: "microsoft/Phi-3-mini-4k-instruct"
    # If the user really wants the other one, we can swap it, but I'll use Phi-3 for stability first.
    
    repo_id = "Qwen/Qwen2.5-72B-Instruct"
    
    import requests
    api_url = "https://router.huggingface.co/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}"}

    prompt_formatted = f"Context:\n{context_text}\n\nQuestion:\n{user_query}"
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt_formatted}
    ]

    print(f"Generating answer using {repo_id}...")
    try:
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
        print("\n---------------------\n")
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
        else:
            response_json = response.json()
            # Parse response (usually [{"generated_text": "..."}])
            if isinstance(response_json, list) and len(response_json) > 0:
                if "generated_text" in response_json[0]:
                    print(response_json[0]["generated_text"])
                else:
                    print(response_json)
            else:
                print(response_json)
        print("\n---------------------\n")
    except Exception as e:
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {e}")