from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os
import rag_engine

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def read_root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")

class QueryRequest(BaseModel):
    query: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"data/{file.filename}"
        os.makedirs("data", exist_ok=True)
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
            
        # Process the PDF
        success = rag_engine.process_pdf(file_location)
        
        if success:
            return JSONResponse(content={"message": "File uploaded and processed successfully!"}, status_code=200)
        else:
            raise HTTPException(status_code=500, detail="Failed to process PDF.")
            
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=500)

@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        answer = rag_engine.get_answer(request.query)
        return JSONResponse(content={"answer": answer}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
