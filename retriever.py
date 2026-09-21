import json
import os
import requests

EMBEDDING_URL = "http://localhost:1234/v1/embeddings"
EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v1.5"


def load_documents(knowledge_dir):
    documents = []

    for filename in os.listdir(knowledge_dir):
        if filename.endswith(".md"):
            path = os.path.join(knowledge_dir, filename)

            with open(path, encoding="utf-8") as f:
                content = f.read()

            documents.append({
                "filename": filename,
                "content": content
            })
    return documents


def semantic_retrieve(query, embedded_chunks, top_k=3):
    query_embedding = get_embedding(query)
    scored_chunks = []

    for chunk in embedded_chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])

        scored_chunks.append({
            "score": score,
            "source": chunk["source"],
            "section": chunk["section"],
            "content": chunk["content"],
        })
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]


def chunk_document(document):
    chunks = []

    sections = document["content"].split("\n## ")

    for section in sections[1:]:
        if not section.strip():
            continue

        lines = section.split("\n", maxsplit=1)
        title = lines[0].strip()

        if len(lines) > 1:
            content = lines[1].strip()
        else:
            content = ""

        chunks.append({
            "source": document["filename"],
            "section": title,
            "content": content,
        })
    return chunks


def cosine_similarity(embedding1, embedding2):
    dot_product = sum(a * b for a, b in zip(embedding1, embedding2))

    magnitude1 = sum(a * a for a in embedding1) ** 0.5
    magnitude2 = sum(b * b for b in embedding2) ** 0.5

    return dot_product / (magnitude1 * magnitude2)


def retrieve(query, chunks):
    query_words = set(query.lower().split())
    scored_chunks = []

    for chunk in chunks:
        text = chunk["section"] + " " + chunk["content"]
        chunk_words = set(text.lower().split())

        score = len(query_words & chunk_words)

        scored_chunks.append({
            "score": score,
            "source": chunk["source"],
            "section": chunk["section"],
            "content": chunk["content"],
        })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks


def get_embedding(text):
    response = requests.post(
        EMBEDDING_URL,
        json = {"model": EMBEDDING_MODEL, "input": text},
        timeout = 30,
    )

    response.raise_for_status()
    data = response.json()
    return data["data"][0]["embedding"]


def embed_chunks(chunks):
    embedded_chunks = []

    for chunk in chunks:
        text = chunk["section"] + " " + chunk["content"]
        embedding = get_embedding(text)

        embedded_chunks.append({
            "source": chunk["source"],
            "section": chunk["section"],
            "content": chunk["content"],
            "embedding": embedding
        })
    return embedded_chunks


def save_index(embedded_chunks, index_path):
    data = {"embedding_model": EMBEDDING_MODEL, "chunks": embedded_chunks}

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def load_index(index_path):
    with open(index_path, encoding="utf-8") as f:
        return json.load(f)
