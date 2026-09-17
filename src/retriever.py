import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


INDEX_FILE = Path("data/index/faiss.index")
METADATA_FILE = Path("data/index/metadata.json")


index = faiss.read_index(str(INDEX_FILE))


with open(METADATA_FILE, "r", encoding="utf-8") as file:
    chunks = json.load(file)


model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query, top_k=5, score_threshold=0.5):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = query_embedding.astype("float32")

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, index_id in zip(scores[0], indices[0]):
        if index_id == -1:
            continue

        if score < score_threshold:
            continue

        chunk = chunks[index_id]

        results.append({
            "score": float(score),
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "page_start": chunk["page_start"],
            "page_end": chunk["page_end"],
            "text": chunk["text"]
        })

    return results


if __name__ == "__main__":
    query = input("Ask a question: ")

    results = search(query)

    print()
    print("=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)

    if not results:
        print()
        print("No sufficiently relevant document context found.")
        print("Try asking a question related to the document.")
    else:
        for i, result in enumerate(results, start=1):
            print()
            print(f"RESULT {i}")
            print(f"Score: {result['score']:.4f}")
            print(f"Chunk ID: {result['chunk_id']}")
            print(f"Source: {result['source']}")
            print(
                f"Pages: {result['page_start']}-{result['page_end']}"
            )
            print("-" * 60)
            print(result["text"][:1000])