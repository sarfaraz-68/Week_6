import os
import logging
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential


load_dotenv()


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    logger.error("GEMINI_API_KEY is missing")
    raise ValueError("GEMINI_API_KEY is not set in the .env file")


client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=4
    )
)
def call_gemini(prompt):
    logger.info("Sending request to Gemini")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        logger.info("Gemini response received")

        return response.text

    except Exception as error:
        logger.error("Gemini request failed: %s", error)
        raise


@lru_cache(maxsize=100)
def generate_cached_answer(question, context):
    logger.info("Generating new answer - cache miss")

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the provided document context.

If the answer is not present in the context, say:

"I could not find this information in the provided document."

Do not use outside knowledge.
Do not invent facts.

When possible, mention the relevant page number.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    return call_gemini(prompt)


def generate_answer(question, retrieved_chunks):
    logger.info("Question received: %s", question)

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"Source: {chunk['source']}\n"
            f"Pages: {chunk['page_start']}-{chunk['page_end']}\n"
            f"Content:\n{chunk['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    before = generate_cached_answer.cache_info()

    answer = generate_cached_answer(
        question,
        context
    )

    after = generate_cached_answer.cache_info()

    if after.hits > before.hits:
        logger.info("Cache hit")

    else:
        logger.info("Cache miss")

    logger.info("Answer generated successfully")

    return answer


if __name__ == "__main__":
    print("Generator module loaded successfully.")