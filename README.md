# Local LLM CLI

A small Python CLI for sending prompts to a local LLM running through LM Studio.

## Requirements

- Python 3.11+
- LM Studio
- A local model loaded in LM Studio

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

```bash
python app.py What is Kubernetes
```

The CLI returns the model response and available inference statistics.

## Testing

```bash
python -m pytest
```

Tests cover successful requests, request failures, invalid JSON, and unexpected response formats.

## Project structure

```text
llm-learning/
├── app.py
├── requirements.txt
├── .gitignore
└── tests/
    └── test_app.py
```

Part of a broader project exploring practical LLM engineering, including log investigation, RAG, and tool calling.
