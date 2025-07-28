from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.evaluate_decision import evaluate_claim
import json
from fastapi import UploadFile, File, Form
from fastapi.responses import JSONResponse
from utils.pdf_utils import extract_text_from_pdf

@app.post("/upload_and_query")
async def upload_and_query(file: UploadFile = File(...), query: str = Form(...)):
    try:
        contents = await file.read()
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(contents)

        extracted_text = extract_text_from_pdf("temp_uploaded.pdf")

        # Save as .txt so FAISS indexing works
        with open("data/uploaded_doc.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)

        # Re-ingest for this new document
        from src.ingest_documents import chunk_and_embed_documents
        chunk_and_embed_documents(doc_folder="data/")

        # Now process the query
        response = evaluate_claim(query)

        try:
            return JSONResponse(content=json.loads(response))
        except Exception:
            return {"error": "Could not parse LLM output", "raw_output": response}

    except Exception as e:
        return {"error": str(e)}

