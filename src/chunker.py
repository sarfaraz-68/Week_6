from pathlib import Path
import json

from pypdf import PdfReader


# Folder containing our PDF documents.
DOCUMENTS_DIR = Path("data/documents")


# Folder where processed chunks will be stored.
CHUNKS_DIR = Path("data/chunks")


# Final JSON file containing our chunks.
CHUNKS_FILE = CHUNKS_DIR / "chunks.json"


# Maximum number of characters in one chunk.
CHUNK_SIZE = 1000


# Number of characters shared between consecutive chunks.
OVERLAP = 200


# Ignore chunks that contain fewer than this many characters.
MIN_CHUNK_SIZE = 100


def load_pages(file_path):
    """
    Read the PDF one page at a time.
    """

    # Open the PDF.
    reader = PdfReader(file_path)

    # Store extracted pages here.
    pages = []

    # Go through every page.
    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):

        # Extract text from the page.
        page_text = page.extract_text()

        # If the page contains no extractable text,
        # skip it.
        if not page_text:
            continue

        # Remove unnecessary whitespace.
        page_text = page_text.strip()

        # If nothing remains after cleaning,
        # skip the page.
        if not page_text:
            continue

        # Store page information.
        pages.append(
            {
                "page": page_number,
                "text": page_text,
                "source": file_path.name,
            }
        )

    return pages


def create_chunks(pages):
    """
    Convert PDF pages into chunks.

    Each chunk contains:
    - chunk_id
    - source
    - page_start
    - page_end
    - text
    """

    # This list will contain all chunks.
    chunks = []

    # Give every chunk a unique ID.
    chunk_id = 0

    # Process every extracted page.
    for page in pages:

        # Get the page's text.
        text = page["text"]

        # Start at the beginning of the page.
        start = 0

        # Total number of characters on this page.
        text_length = len(text)

        # Continue until the entire page is processed.
        while start < text_length:

            # Calculate the end of this chunk.
            end = min(
                start + CHUNK_SIZE,
                text_length,
            )

            # Extract the chunk text.
            chunk_text = text[start:end].strip()

            # Only keep chunks containing enough text.
            if len(chunk_text) >= MIN_CHUNK_SIZE:

                # Create a new chunk ID.
                chunk_id += 1

                # Store content + metadata.
                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "source": page["source"],
                        "page_start": page["page"],
                        "page_end": page["page"],
                        "text": chunk_text,
                    }
                )

            # If this was the final part of the page,
            # stop processing this page.
            if end >= text_length:
                break

            # Move forward while keeping overlap.
            next_start = end - OVERLAP

            # Safety check to guarantee progress.
            if next_start <= start:
                next_start = end

            # Continue from the new position.
            start = next_start

    return chunks


def save_chunks(chunks):
    """
    Save chunks to a JSON file.
    """

    # Create data/chunks if it doesn't exist.
    CHUNKS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Open the output file.
    with open(
        CHUNKS_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        # Convert Python objects into JSON.
        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2,
        )


def print_chunks(chunks, number_to_show=5):
    """
    Display a few chunks for inspection.
    """

    print("\n" + "=" * 60)

    print(f"Total chunks: {len(chunks)}")

    print("=" * 60)

    # Only display the first few chunks.
    for chunk in chunks[:number_to_show]:

        print("\n" + "=" * 60)

        print(
            f"CHUNK ID: "
            f"{chunk['chunk_id']}"
        )

        print(
            f"SOURCE: "
            f"{chunk['source']}"
        )

        print(
            f"PAGES: "
            f"{chunk['page_start']}"
            f"-"
            f"{chunk['page_end']}"
        )

        print("=" * 60)

        print(chunk["text"])


def main():

    # Find PDFs in our documents folder.
    pdf_files = list(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    # Stop if no PDF exists.
    if not pdf_files:

        print("No PDF files found.")

        return

    # We are using one PDF for this project.
    for pdf_file in pdf_files:

        print("\n" + "=" * 60)

        print(
            f"FILE: "
            f"{pdf_file.name}"
        )

        print("=" * 60)

        # Extract pages.
        pages = load_pages(pdf_file)

        print(
            f"Pages loaded: "
            f"{len(pages)}"
        )

        # Create chunks.
        chunks = create_chunks(pages)

        print(
            f"Chunks created: "
            f"{len(chunks)}"
        )

        # Save chunks.
        save_chunks(chunks)

        print(
            f"Saved to: "
            f"{CHUNKS_FILE}"
        )

        # Display some chunks.
        print_chunks(chunks)


if __name__ == "__main__":
    main()