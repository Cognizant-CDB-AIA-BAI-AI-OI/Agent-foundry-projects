# fast_api_app.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
import os

from utils import setup_env_and_llm                        # Initializes environment and language model
from pdf_qa import pdf_text_extraction, pdf_query          # Functions for extracting text and querying PDFs
from inputs import model, prompt                       # Imported input values

# STEP 1: Set up the LLM client and config
client, generate_content_config = setup_env_and_llm()

app = FastAPI(title="📄 PDF Question Answering API")

@app.post("/query-pdf")
async def query_pdf(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # STEP 2: Extract PDF content
        context = pdf_text_extraction(temp_path)

        # STEP 3: Query the model
        response = pdf_query(
            context,
            prompt,
            client,
            generate_content_config,
            model
        )

        os.remove(temp_path)

        return JSONResponse(content={"response": response})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Launch with: python fast_api_app.py
if __name__ == "__main__":
    uvicorn.run("fast_api_app:app", host="127.0.0.1", port=8000, reload=False)
