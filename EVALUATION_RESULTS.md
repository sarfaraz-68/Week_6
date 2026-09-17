# Evaluation Results

## 1. Evaluation Overview

This project includes an evaluation harness to measure the quality of the RAG system.

The evaluation is not based only on manually checking a few answers. Instead, the system runs a repeatable set of test questions and produces measurable results.

The evaluation includes:

- 15 total test cases
- 12 answerable questions
- 3 unanswerable questions
- Rule-based evaluation
- LLM-as-a-judge evaluation
- Regression testing

---

## 2. Test Cases

The evaluation dataset contains 15 questions.

### Answerable Questions

These questions should be answered using information from the sanitation document.

Examples include:

- What are the health benefits of safe sanitation?
- What diseases are associated with poor sanitation?
- How does sanitation affect mental and social well-being?
- How can poor sanitation affect children?
- What is the definition of sanitation according to the document?

### Unanswerable Questions

These questions are not related to information in the provided document.

Examples include:

- What is the population of Japan?
- What is the capital city of France?
- Who won the FIFA World Cup in 2022?

For these questions, the correct behaviour is to refuse and say:

"I could not find this information in the provided document."

---

## 3. Rule-Based Evaluation

The rule-based evaluation checks whether the system follows expected behaviour.

For answerable questions, it checks:

1. Whether important expected facts appear in the answer.
2. Whether the answer includes a page or source citation.

For unanswerable questions, it checks:

1. Whether the system correctly refuses to answer.

The rule-based evaluation is useful because it is:

- Fast
- Free
- Repeatable
- Deterministic

However, it has limitations.

For example, an answer can be correct but still fail if it uses different wording from the expected key facts.

---

## 4. LLM-as-a-Judge Evaluation

The project also uses an LLM to evaluate answer quality.

The judge receives:

- The original question
- The generated system answer

The judge gives:

- A score from 1 to 5
- A short explanation for the score

This helps evaluate qualities that keyword matching cannot fully measure, such as:

- Relevance
- Correctness
- Completeness
- Overall answer quality

The LLM judge is not perfect, so its results should be manually spot-checked.

---

## 5. Normal System Results

With the normal retrieval configuration, the system produced the following results:

```text
Rule-based Passed: 11/15
Rule-based Accuracy: 73.33%
LLM Judge Average: 5.00/5