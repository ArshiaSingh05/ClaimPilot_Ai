'''
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import glob
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from utils.pdf_utils import extract_text_from_pdf  # Import from utils

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_and_embed_documents(doc_folder='data/'):
    documents = []
    metadata = []

    # Scan all .txt and .pdf files
    for file_path in glob.glob(os.path.join(doc_folder, '*')):
        if file_path.endswith(".txt"):
            print(f"[INFO] Loading TXT file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif file_path.endswith(".pdf"):
            print(f"[INFO] Loading PDF file: {file_path}")
            text = extract_text_from_pdf(file_path)
        else:
            continue  # skip other files

        # Chunk by line (each clause)
        chunks = [line.strip() for line in text.split('\n') if line.strip()]
        documents.extend(chunks)
        metadata.extend([
            {"source": os.path.basename(file_path), "clause": i}
            for i in range(len(chunks))
        ])

    print("[DEBUG] Number of document chunks:", len(documents))
    for i, doc in enumerate(documents):
        print(f"Chunk {i+1}: {doc}")

    if not documents:
        print("[ERROR] No valid documents found. Ensure .txt or .pdf files are placed in the folder.")
        return

    # Create embeddings
    embeddings = model.encode(documents, convert_to_numpy=True)
    dim = embeddings.shape[1]

    # Build FAISS index
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index and metadata
    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, "embeddings/faiss_index.idx")
    with open("embeddings/metadata.pkl", "wb") as f:
        pickle.dump((documents, metadata), f)

    print(f"[✓] Embedded {len(documents)} document chunks.")

if __name__ == "__main__":
    chunk_and_embed_documents()
'''