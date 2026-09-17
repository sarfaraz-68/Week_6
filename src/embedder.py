import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


CHUNKS_FILE = Path("data/chunks/chunks.json")
INDEX_FILE = Path("data/index/faiss.index")
METADATA_FILE = Path("data/index/metadata.json")


INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)


with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
    chunks = json.load(file)

print(f"Loaded {len(chunks)} chunks")


texts = [chunk["text"] for chunk in chunks]


model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded")


embeddings = model.encode(
    texts,
    show_progress_bar=True,
    normalize_embeddings=True
)


embeddings = embeddings.astype("float32")


dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)


index.add(embeddings)


faiss.write_index(index, str(INDEX_FILE))


with open(METADATA_FILE, "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)


print()
print("=" * 60)
print("EMBEDDING COMPLETE")
print("=" * 60)
print(f"Chunks:     {len(chunks)}")
print(f"Dimensions: {dimension}")
print(f"FAISS:      {INDEX_FILE}")
print(f"Metadata:   {METADATA_FILE}")
print("=" * 60)