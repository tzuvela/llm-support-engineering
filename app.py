import argparse
import requests

API_URL = "http://localhost:1234/api/v1/chat"
MODEL = "qwen3.5-2b"


def ask_llm(prompt):
    body = {
        "model": MODEL,
        "input": prompt,
        "reasoning": "off",
        "store": False,
    }

    try:
        response = requests.post(API_URL, json=body, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
    except ValueError as e:
        print("Invalid JSON response:", e)
        return None


def print_response(data):
    try:
        answer = data["output"][0]["content"]
    except (KeyError, IndexError, TypeError) as e:
        print("Unexpected response format:", e)
        return

    print("Answer:", answer)

    stats = data.get("stats", {})

    input_tokens = stats.get("input_tokens", "unavailable")
    output_tokens = stats.get("total_output_tokens", "unavailable")
    reasoning_tokens = stats.get("reasoning_output_tokens", "unavailable")
    tokens_per_second = stats.get("tokens_per_second", "unavailable")
    ttft = stats.get("time_to_first_token_seconds", "unavailable")

    print("Input tokens:", input_tokens)
    print("Output tokens:", output_tokens)
    print("Reasoning tokens:", reasoning_tokens)
    print("Tokens per second:", tokens_per_second)
    print("TTFT:", ttft)


def main():
    parser = argparse.ArgumentParser(description="Ask a local LLM a question")
    parser.add_argument("prompt", nargs="+", help="The question to send to the LLM")
    args = parser.parse_args()

    prompt = " ".join(args.prompt)
    data = ask_llm(prompt)

    if data is not None:
        print_response(data)


if __name__ == "__main__":
    main()