from pathlib import Path

from pypdf import PdfReader


DOCUMENTS_DIR = Path("data/documents")


def load_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


if __name__ == "__main__":
    for pdf_file in DOCUMENTS_DIR.glob("*.pdf"):
        text = load_pdf(pdf_file)

        print("=" * 60)
        print(f"FILE: {pdf_file.name}")
        print("=" * 60)
        print(text[:2000])