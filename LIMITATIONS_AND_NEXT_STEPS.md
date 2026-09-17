# Limitations and Next Steps

## Current Limitations

The current application is a working RAG-based document question-answering system, but it still has some limitations.

### 1. Retrieval Can Miss Relevant Information

The system depends on the retriever finding the correct document chunks.

If the similarity threshold is too high, relevant chunks may not be retrieved.

This was demonstrated during evaluation when the retrieval threshold was changed from 0.5 to 0.9. The evaluation score dropped significantly.

### 2. Rule-Based Evaluation Is Limited

The rule-based evaluator checks whether expected key facts appear in the generated answer.

This can produce false failures when the answer is correct but uses different wording.

For example, the document may say "mental and social well-being" while the generated answer uses slightly different wording.

### 3. LLM-as-a-Judge Is Not Perfect

The LLM judge provides a useful second evaluation of answer quality, but it can also make mistakes.

Its scores should therefore be manually spot-checked.

### 4. Gemini API Quota

The application uses the Gemini API for answer generation and LLM-based evaluation.

The free API quota is limited, so running many evaluations can exhaust the available requests.

Caching helps reduce repeated API calls, but the application still depends on the available API quota.

### 5. Local Embedding Model

The application uses the `all-MiniLM-L6-v2` sentence-transformer model for retrieval.

The model runs locally, but loading the model can take time when the application starts.

### 6. Single Document Focus

The current application is designed around the provided sanitation document.

It is not yet designed as a general multi-document knowledge system.

---

## Production Improvements

The following improvements could be added in a future version.

### 1. Improve Retrieval

Possible improvements include:

* Testing different similarity thresholds
* Improving chunk sizes
* Using a stronger embedding model
* Adding hybrid keyword and vector search
* Reranking retrieved chunks

### 2. Improve Evaluation

The evaluation system could be improved by:

* Adding more test cases
* Adding more difficult questions
* Improving key-fact matching
* Adding separate scores for correctness, relevance, and citation quality
* Performing regular manual spot-checks of LLM judge results

### 3. Reduce API Usage

To reduce Gemini API usage:

* Keep response caching enabled
* Avoid unnecessary repeated evaluations
* Use local models where appropriate
* Run smaller evaluation subsets during development

### 4. Improve Error Handling

The application already uses retries for temporary API failures.

A future production version could also provide clearer handling for:

* API quota exhaustion
* Invalid API responses
* Network failures
* Missing configuration
* Retrieval failures

### 5. Improve User Interface

The current Streamlit interface is intentionally simple.

Future versions could add:

* File upload
* Multiple document support
* Source-document previews
* Conversation history
* Better citation display
* Retrieval confidence information

---

## Final Assessment

The project currently demonstrates the main requirements of the Week 6 capstone:

* LLM-based answer generation
* Retrieval-augmented generation
* Real document data
* Evaluation with rule-based checks
* Evaluation with an LLM judge
* Error handling and retries
* Response caching
* Logging
* Environment-based secret management

The main remaining improvements are focused on making retrieval, evaluation, API usage, and the user experience more robust.
