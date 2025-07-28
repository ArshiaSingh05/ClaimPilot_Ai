import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index
index = faiss.read_index("embeddings/faiss_index.idx")

# Load metadata: list of clause texts + info
with open("embeddings/metadata.pkl", "rb") as f:
    documents, metadata = pickle.load(f)

def semantic_search(query, top_k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i in range(top_k):
        idx = indices[0][i]
        result = {
            "clause_text": documents[idx],
            "source_file": metadata[idx]["source"],
            "clause_number": metadata[idx]["clause"],
            "similarity_score": round(1 / (1 + float(distances[0][i])), 3),
            "raw_distance": float(distances[0][i])
        }
        results.append(result)

    return results

# Test
if __name__ == "__main__":
    test_query = "knee surgery in Pune"
    results = semantic_search(test_query)

    print(" Top Relevant Clauses:\n")
    for r in results:
        print(f"Clause: {r['clause_text']}")
        print(f"Source: {r['source_file']} | Clause #: {r['clause_number']} | Score: {r['similarity_score']:.2f} | distance: {r['raw_distance']:.2f}")
        print("---")
