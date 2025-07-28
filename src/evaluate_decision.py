import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.parse_query import parse_query
from src.semantic_search import semantic_search
from src.local_llm import local_llm_response
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
# Load the sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_prompt(parsed_query, retrieved_clauses):
    context = "\n".join([f"- {r['clause_text']}" for r in retrieved_clauses])
    prompt = f"""
You are a health insurance assistant.

Given the following user query and retrieved policy clauses, decide:

- Whether the procedure is approved or rejected
- If approved, provide the amount covered (if mentioned)
- Justify your decision by referencing one or more clauses

User Query (Parsed):
- Age: {parsed_query['age']}
- Gender: {parsed_query['gender']}
- Procedure: {parsed_query['procedure']}
- Location: {parsed_query['location']}
- Policy Duration: {parsed_query['policy_duration']}

Relevant Clauses:
{context}

Respond in the following JSON format:
{{
  "decision": "...",
  "amount": "...",
  "justification": "... (include clause references)"
}}
"""
    return prompt

def evaluate_claim(query, context=None):
    if context:
        # Chunk the uploaded PDF text (by line or para)
        chunks = [line.strip() for line in context.split('\n') if line.strip()]
        
        if not chunks:
            return {"error": "No valid clauses found in uploaded PDF."}

        # Embed chunks
        embeddings = model.encode(chunks, convert_to_numpy=True)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        # Embed the query
        query_vec = model.encode([query])
        D, I = index.search(query_vec, k=3)

        top_chunks = [chunks[i] for i in I[0]]
        print("[DEBUG] Top relevant clauses:", top_chunks)

        # Prepare prompt for LLM
        context_for_llm = "\n".join(top_chunks)
        final_prompt = f"User Query: {query}\nRelevant Clauses:\n{context_for_llm}\nAnswer the query in structured JSON format."

        # Replace this with your LLM call (or mock if testing)
        from ollama import chat
        response = chat(model="mistral", messages=[{"role": "user", "content": final_prompt}])

        return response['message']['content']
    
    else:
        return {"error": "No context provided and fallback index not allowed."}


if __name__ == "__main__":
    test_query = "46-year-old male, knee surgery in Pune, 3-month-old policy"
    output = evaluate_claim(test_query)
    print(" Final Output from LLM:\n")
    print(output)