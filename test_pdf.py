from pdf_processor import extract_text_from_pdf

pdf_path = "data/sample.pdf"

try:
    text = extract_text_from_pdf(pdf_path)

    print("\nPDF TEXT EXTRACTION SUCCESSFUL!")
    print("--------------------------------")
    print(text[:2000])

except Exception as e:
    print("Error:", e)