import rag_engine
import os

# Check if vectorstore is already initialized
if rag_engine.vectorstore:
    print("Vectorstore already loaded")
else:
    print("No vectorstore found - need to upload a PDF first")
    
# Test query
test_query = "What vegetables are mentioned?"
print(f"\nQuery: {test_query}")
answer = rag_engine.get_answer(test_query)
print(f"\nAnswer:\n{answer}")
print(f"\nAnswer type: {type(answer)}")
print(f"Answer length: {len(answer)}")
