import os
import pdfplumber
from PyPDF2 import PdfMerger

def merge_pdfs(input_folder, output_folder, output_filename):
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    pdf_files = sorted([
        f for f in os.listdir(input_folder)
        if f.lower().endswith('.pdf')
    ])

    if not pdf_files:
        print("No PDF files found in the upload folder.")
        return None

    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(os.path.join(input_folder, pdf))

    merged_path = os.path.join(output_folder, output_filename)
    merger.write(merged_path)
    merger.close()

    print(f"Merged PDF saved to: {merged_path}")
    return merged_path

def extract_text_with_plumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

if __name__ == "__main__":
    input_folder = "upload"
    output_folder = "result"
    merged_pdf_name = "merged.pdf"
    text_output_name = "extracted_text.txt"

    # Step 1: Merge PDFs
    merged_pdf_path = merge_pdfs(input_folder, output_folder, merged_pdf_name)

    # Step 2: Extract text using pdfplumber
    if merged_pdf_path and os.path.exists(merged_pdf_path):
        extracted_text = extract_text_with_plumber(merged_pdf_path)

        # Step 3: Save to TXT file
        txt_path = os.path.join(output_folder, text_output_name)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"Extracted text saved to: {txt_path}")
