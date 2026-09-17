from retriever import search
from generator import generate_answer


def ask_question(question):
    retrieved_chunks = search(
        question,
        top_k=5,
        score_threshold=0.5
    )

    if not retrieved_chunks:
        return "I could not find this information in the provided document."

    answer = generate_answer(
        question,
        retrieved_chunks
    )

    return answer


if __name__ == "__main__":
    question = input("Ask a question: ")

    answer = ask_question(question)

    print()
    print("=" * 60)
    print("ANSWER")
    print("=" * 60)
    print()
    print(answer)