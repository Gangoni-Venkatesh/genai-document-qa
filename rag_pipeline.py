
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from pdf_processor import extract_pages_from_pdf
from text_splitter import split_documents
from vector_store import create_vector_store


# Load environment variables
load_dotenv(override=True)


# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.3
)


def create_rag_pipeline(pdf_path, source_name=None):
    """
    Create a RAG pipeline using PDF, FAISS and Gemini.
    """

    # Extract pages with metadata
    documents = extract_pages_from_pdf(
        pdf_path,
        source_name=source_name
    )

    # Split documents while preserving metadata
    chunks = split_documents(documents)

    # Create FAISS vector store
    vector_store = create_vector_store(chunks)

    return vector_store


def ask_question(vector_store, question):
    """
    Retrieve relevant document content,
    generate an answer and return source references.
    """

    # Retrieve relevant chunks
    documents = vector_store.similarity_search(
        question,
        k=3
    )

    # Prepare context with source information
    context_parts = []

    for document in documents:

        source = document.metadata.get("source", "Unknown")
        page = document.metadata.get("page", "Unknown")

        context_parts.append(
            f"Source: {source}, Page: {page}\n"
            f"Content: {document.page_content}"
        )

    context = "\n\n".join(context_parts)

    # Create prompt
    prompt = f"""
    You are an AI assistant that answers questions
    based only on the provided document context.

    If the answer is not available in the context,
    clearly say that the information is not available
    in the uploaded documents.

    Do not invent information.

    Document Context:
    {context}

    User Question:
    {question}

    Answer:
    """

    # Generate answer using Gemini
    response = llm.invoke(prompt)

    # Extract readable answer
    if isinstance(response.content, list):

        answer = "\n".join(
            item["text"]
            for item in response.content
            if isinstance(item, dict)
            and item.get("type") == "text"
        )

    else:
        answer = response.content

    # Collect unique source references
    sources = []

    for document in documents:

        source_info = {
            "source": document.metadata.get("source", "Unknown"),
            "page": document.metadata.get("page", "Unknown"),
            "content": document.page_content
        }

        if not any(
            item["source"] == source_info["source"]
            and item["page"] == source_info["page"]
            for item in sources
        ):
            sources.append(source_info)

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":

    print("Creating RAG pipeline...")

    vector_store = create_rag_pipeline(
        "data/sample.pdf",
        source_name="sample.pdf"
    )

    print("\nRAG PIPELINE CREATED SUCCESSFULLY!")

    question = "What are my technical skills?"

    result = ask_question(vector_store, question)

    print("\nGEMINI ANSWER:")
    print(result["answer"])

    print("\nSOURCE REFERENCES:")

    for source in result["sources"]:
        print(
            f"File: {source['source']} | "
            f"Page: {source['page']}"
        )
