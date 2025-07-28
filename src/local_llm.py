import requests

def local_llm_response(prompt, model="mistral"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        return response.json()["response"]
    except Exception as e:
        return f"[ERROR] LLM call failed: {e}"
