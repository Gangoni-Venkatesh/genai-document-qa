from pdf_processor import extract_text_from_pdf
from text_splitter import split_text
from embeddings import generate_embeddings

# Extract PDF text
text = extract_text_from_pdf("data/sample.pdf")

# Split text
chunks = split_text(text)

# Generate embeddings
embeddings = generate_embeddings(chunks)

print("\nEMBEDDING GENERATION SUCCESSFUL!")
print("--------------------------------")

print("Total chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

print("\nFirst chunk embedding:")
print(embeddings[0][:10])