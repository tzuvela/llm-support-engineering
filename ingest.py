import retriever

KNOWLEDGE_DIR = "knowledge"
INDEX_PATH = "knowledge/index.json"


def build_index():
    documents = retriever.load_documents(KNOWLEDGE_DIR)
    all_chunks = []

    for document in documents:
        chunks = retriever.chunk_document(document)
        all_chunks.extend(chunks)

    embedded_chunks = retriever.embed_chunks(all_chunks)

    retriever.save_index(embedded_chunks, INDEX_PATH)

    print(f"Indexed {len(documents)} documents.")
    print(f"Created {len(all_chunks)} chunks.")
    print(f"Saved index to {INDEX_PATH}")


if __name__ == "__main__":
    build_index()