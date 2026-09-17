# Architecture Write-up

## 1. Project Overview

This project is a Sanitation Document Question and Answer application.

The user asks a question about a sanitation document. The system searches the document for relevant information and then uses Gemini to generate an answer based only on the retrieved information.

This approach is called Retrieval-Augmented Generation (RAG).

The application can be used through:

- A command-line interface using `rag_pipeline.py`
- A web interface using Streamlit

---

## 2. Main Architecture

```text
User
  |
  v
Streamlit App / Command Line
  |
  v
RAG Pipeline
  |
  v
Retriever
  |
  +--> SentenceTransformer creates question embedding
  |
  +--> FAISS searches document embeddings
  |
  v
Relevant Document Chunks
  |
  v
Generator
  |
  +--> Builds prompt with document context
  |
  +--> Checks cache
  |
  +--> Retries failed API calls
  |
  +--> Sends request to Gemini
  |
  v
Final Answer
  |
  v
User