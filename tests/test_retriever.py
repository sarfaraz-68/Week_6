import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from retriever import search


def test_relevant_question_finds_document_chunks():
    results = search(
        "What are the health benefits of safe sanitation?",
        top_k=5,
        score_threshold=0.5
    )

    assert len(results) > 0


def test_unrelated_question_finds_no_chunks():
    results = search(
        "What is the population of Japan?",
        top_k=5,
        score_threshold=0.5
    )

    assert len(results) == 0