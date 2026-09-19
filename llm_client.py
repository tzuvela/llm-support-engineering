import argparse
import requests

API_URL = "http://localhost:1234/api/v1/chat"
MODEL = "qwen3.5-4b"


def ask_llm(prompt):
    body = {
        "model": MODEL,
        "input": prompt,
        "reasoning": "on",
        "store": False,
    }

    try:
        response = requests.post(API_URL, json=body, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data, MODEL
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
    except ValueError as e:
        print("Invalid JSON response:", e)
        return None
