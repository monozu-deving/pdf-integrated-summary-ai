import os
from PyPDF2 import PdfMerger

def merge_pdfs(input_folder='upload', output_folder='result', output_filename='merged.pdf'):
    # 폴더 존재 확인 및 생성
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # PDF 파일 목록 가져오기 및 이름순 정렬
    pdf_files = sorted([
        f for f in os.listdir(input_folder)
        if f.lower().endswith('.pdf')
    ])

    if not pdf_files:
        print("No PDF files found in the upload folder.")
        return

    merger = PdfMerger()

    for pdf in pdf_files:
        pdf_path = os.path.join(input_folder, pdf)
        merger.append(pdf_path)

    output_path = os.path.join(output_folder, output_filename)
    merger.write(output_path)
    merger.close()

    print(f"Merged PDF saved to: {output_path}")

if __name__ == "__main__":
    merge_pdfs()
