
from pdf_processor import extract_pages_from_pdf
from text_splitter import split_documents
from vector_store import create_vector_store


# Extract PDF pages
documents = extract_pages_from_pdf("data/sample.pdf")

# Split documents into chunks
chunks = split_documents(documents)

# Create FAISS vector database
vector_store = create_vector_store(chunks)

# Search for relevant information
query = "What are my technical skills?"

results = vector_store.similarity_search(query, k=3)

print("\nFAISS SEARCH WITH METADATA SUCCESSFUL!")
print("--------------------------------------")

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}:")
    print("Source:", result.metadata["source"])
    print("Page:", result.metadata["page"])
    print("Content:", result.page_content[:300])
