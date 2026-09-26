import requests

API_URL = "http://localhost:1234/api/v1/chat"
CHAT_API_URL = "http://localhost:1234/v1/chat/completions"
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
        return None, MODEL
    except ValueError as e:
        print("Invalid JSON response:", e)
        return None, MODEL


def chat_completion(messages, tools=None):
    body = {"model": MODEL, "messages": messages}

    if tools is not None:
        body["tools"] = tools

    try:
        response = requests.post(
            CHAT_API_URL,
            json=body,
            timeout = 120,
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print("Request failed", e)
        if e.response is not None:
            print("Response", e.response.text)
        return None
    except ValueError as e:
        print("Invalid JSON response", e)
        return None
