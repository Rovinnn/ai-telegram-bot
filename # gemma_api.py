# gemma_api.py
import requests

def call_local_gemma(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Gemma Error:", e)
        return "⚠️ Sorry, something went wrong with the local model."
