import json
import re
import os

from dotenv import load_dotenv
from google import genai

from retriever import search
from generator import generate_answer


EVALUATION_FILE = "data/evaluation_questions.json"
SCORE_THRESHOLD = 0.5

load_dotenv()

judge_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

JUDGE_MODEL = "gemini-3.5-flash-lite"


def load_questions():
    with open(EVALUATION_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def check_key_facts(answer, key_facts):
    normalized_answer = normalize_text(answer)

    matched = []

    for fact in key_facts:
        normalized_fact = normalize_text(fact)

        if normalized_fact in normalized_answer:
            matched.append(fact)

    return matched


def check_source_citation(answer):
    normalized_answer = normalize_text(answer)

    citation_patterns = [
        "page",
        "pages",
        "source"
    ]

    return any(
        pattern in normalized_answer
        for pattern in citation_patterns
    )


def llm_judge(question, answer, expected):
    prompt = f"""
You are evaluating a document question-answering system.

Evaluate the answer based only on whether it correctly answers the question using the provided document.

Question:
{question}

Expected answer type:
{expected}

System answer:
{answer}

Give a score from 1 to 5.

5 = Excellent answer, correct, relevant, complete, and does not invent information.
4 = Good answer, mostly correct with minor missing details.
3 = Partially correct answer with noticeable missing information.
2 = Mostly incorrect or incomplete answer.
1 = Incorrect answer, irrelevant answer, or hallucinated information.

Return your response in exactly this format:

Score: X
Reason: short explanation
"""

    response = judge_client.models.generate_content(
        model=JUDGE_MODEL,
        contents=prompt
    )

    judge_text = response.text.strip()

    score_match = re.search(
        r"Score:\s*([1-5])",
        judge_text,
        re.IGNORECASE
    )

    if score_match:
        score = int(score_match.group(1))
    else:
        score = 0

    reason_match = re.search(
        r"Reason:\s*(.*)",
        judge_text,
        re.IGNORECASE | re.DOTALL
    )

    if reason_match:
        reason = reason_match.group(1).strip()
    else:
        reason = judge_text

    return score, reason


def evaluate_question(item):
    question = item["question"]
    expected = item["expected"]
    key_facts = item["key_facts"]

    retrieved_chunks = search(
        question,
        top_k=5,
        score_threshold=SCORE_THRESHOLD
    )

    if not retrieved_chunks:
        if expected == "unanswerable":
            return {
                "id": item["id"],
                "question": question,
                "expected": expected,
                "retrieved": False,
                "top_score": 0.0,
                "answer": "I could not find this information in the provided document.",
                "matched_facts": [],
                "fact_score": 0.0,
                "has_citation": False,
                "judge_score": 5,
                "judge_reason": "The system correctly refused because the information was not found in the document.",
                "passed": True
            }

        return {
            "id": item["id"],
            "question": question,
            "expected": expected,
            "retrieved": False,
            "top_score": 0.0,
            "answer": "I could not find this information in the provided document.",
            "matched_facts": [],
            "fact_score": 0.0,
            "has_citation": False,
            "judge_score": 1,
            "judge_reason": "The system failed to retrieve information for an answerable question.",
            "passed": False
        }

    top_score = retrieved_chunks[0]["score"]

    answer = generate_answer(
        question,
        retrieved_chunks
    )

    matched_facts = check_key_facts(
        answer,
        key_facts
    )

    if key_facts:
        fact_score = len(matched_facts) / len(key_facts)
    else:
        fact_score = 0.0

    has_citation = check_source_citation(answer)

    judge_score, judge_reason = llm_judge(
        question,
        answer,
        expected
    )

    if expected == "answerable":
        passed = (
            fact_score >= 0.5
            and has_citation
        )
    else:
        passed = False

    return {
        "id": item["id"],
        "question": question,
        "expected": expected,
        "retrieved": True,
        "top_score": top_score,
        "answer": answer,
        "matched_facts": matched_facts,
        "fact_score": fact_score,
        "has_citation": has_citation,
        "judge_score": judge_score,
        "judge_reason": judge_reason,
        "passed": passed
    }


def main():
    questions = load_questions()

    results = []

    for item in questions:
        print()
        print(f"Evaluating question {item['id']}...")

        result = evaluate_question(item)

        results.append(result)

    print()
    print("=" * 70)
    print("RAG EVALUATION RESULTS")
    print("=" * 70)

    for result in results:
        print()
        print(f"Question {result['id']}")
        print(f"Question:     {result['question']}")
        print(f"Expected:     {result['expected']}")
        print(f"Top Score:    {result['top_score']:.4f}")
        print(f"Fact Score:   {result['fact_score']:.2%}")
        print(
            f"Citation:     "
            f"{'YES' if result['has_citation'] else 'NO'}"
        )
        print(f"LLM Judge:    {result['judge_score']}/5")
        print(f"Judge Reason: {result['judge_reason']}")
        print(
            f"Result:       "
            f"{'PASS' if result['passed'] else 'FAIL'}"
        )

        if result["matched_facts"]:
            print(
                "Matched facts: "
                + ", ".join(result["matched_facts"])
            )

    passed_count = sum(
        1
        for result in results
        if result["passed"]
    )

    total_count = len(results)

    accuracy = (
        passed_count / total_count
        if total_count > 0
        else 0
    )

    judge_scores = [
        result["judge_score"]
        for result in results
        if result["judge_score"] > 0
    ]

    judge_average = (
        sum(judge_scores) / len(judge_scores)
        if judge_scores
        else 0
    )

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Rule-based Passed: {passed_count}/{total_count}")
    print(f"Rule-based Accuracy: {accuracy:.2%}")
    print(f"LLM Judge Average: {judge_average:.2f}/5")
    print("=" * 70)


if __name__ == "__main__":
    main()