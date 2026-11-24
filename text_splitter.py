
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf_processor import extract_pages_from_pdf


def split_documents(documents):
    """
    Split PDF pages into smaller chunks
    while preserving source and page metadata.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def split_text(text):
    """
    Split plain text into smaller chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    return text_splitter.split_text(text)


if __name__ == "__main__":

    documents = extract_pages_from_pdf("data/sample.pdf")

    chunks = split_documents(documents)

    print("DOCUMENT SPLITTING SUCCESSFUL!")
    print("--------------------------------")

    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks, start=1):
        print(f"\nCHUNK {i}")
        print("Metadata:", chunk.metadata)
        print("Content:", chunk.page_content[:150])
