
import os
from pypdf import PdfReader
from langchain_core.documents import Document


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    extracted_text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text += page_text + "\n"

    if not extracted_text.strip():
        raise ValueError("No readable text found in the PDF.")

    return extracted_text


def extract_pages_from_pdf(pdf_path, source_name=None):
    """
    Extract PDF pages and preserve source metadata.
    """

    reader = PdfReader(pdf_path)

    documents = []

    original_name = source_name or os.path.basename(pdf_path)

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text and page_text.strip():

            document = Document(
                page_content=page_text,
                metadata={
                    "source": original_name,
                    "page": page_number
                }
            )

            documents.append(document)

    if not documents:
        raise ValueError("No readable text found in the PDF.")

    return documents


if __name__ == "__main__":
    print("PDF Processor module is ready!")
