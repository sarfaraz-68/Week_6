# Sanitation Document Q&A

A Retrieval-Augmented Generation (RAG) application that answers questions using information from a sanitation document.

The application only uses the provided document context to generate answers. If relevant information is not found, it refuses to answer instead of using outside knowledge.

## Features

- Document-based question answering
- Retrieval-Augmented Generation (RAG)
- FAISS vector search
- SentenceTransformer embeddings
- Gemini LLM for answer generation
- Page-based source information
- Rule-based evaluation
- LLM-as-a-judge evaluation
- Out-of-scope question testing
- Error handling and retries
- Exponential backoff
- Response caching
- Logging
- Environment variable secret management
- Pytest retrieval tests
- Streamlit web interface

## Architecture

The application works as follows:

User Question
    ↓
SentenceTransformer
    ↓
FAISS Retriever
    ↓
Relevant Document Chunks
    ↓
Gemini LLM
    ↓
Final Answer with Page Information

## Project Structure

```text
week6/
├── data/
│   ├── evaluation_questions.json
│   └── index/
│       ├── faiss.index
│       └── metadata.json
│
├── evals/
│
├── src/
│   ├── app.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── evaluate.py
│   ├── generator.py
│   ├── pdf_loader.py
│   ├── rag_pipeline.py
│   └── retriever.py
│
├── tests/
│   └── test_retriever.py
│
├── .env
├── README.md
├── ARCHITECTURE.md
├── EVALUATION_RESULTS.md
└── LIMITATIONS_AND_NEXT_STEPS.md