from pdf_processor import extract_text_from_pdf
from text_splitter import split_text

# Extract text from PDF
text = extract_text_from_pdf("data/sample.pdf")

# Split text into chunks
chunks = split_text(text)

print("TEXT SPLITTING SUCCESSFUL!")
print("--------------------------")

print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\nCHUNK {i}:")
    print(chunk)