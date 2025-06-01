import os
import re
import pdfplumber
from PyPDF2 import PdfMerger
import openai
import subprocess

# 🔑 OpenAI API 키
openai.api_key = "your-api-key-here"

# 경로 설정
input_folder = "upload"
output_folder = "result"
merged_pdf_name = "merged.pdf"
text_file = "extracted_text.txt"
markdown_file = "summary.md"
pdf_file = "summary.pdf"

def merge_pdfs(input_folder, output_path):
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')])
    if not pdf_files:
        print("❌ PDF 파일이 없습니다.")
        return None

    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(os.path.join(input_folder, pdf))
    merger.write(output_path)
    merger.close()
    print(f"✅ 병합 완료: {output_path}")
    return output_path

def extract_text_with_plumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    print("✅ 텍스트 추출 완료")
    return text

def wrap_latex_equations(text):
    # 일반적인 수식 패턴 감지 및 $...$로 감싸기
    patterns = [
        r'\bE\s*=\s*mc\^?2\b',
        r'\b[a-zA-Z]+\^2\b',
        r'\b\\int.*?dx\b',
        r'\b[a-zA-Z]+\s*=\s*[^ \n]+',  # a = b 형식
        r'\b\d+\s*\^\s*\d+\b',         # 2^3, 10^2 등
        r'\\frac{.*?}{.*?}',           # \frac{}{}
    ]
    for pat in patterns:
        text = re.sub(pat, lambda m: f"${m.group(0)}$", text)
    return text

def summarize_with_gpt(text):
    prompt = f"""다음 텍스트에는 $...$ 형식으로 감싼 수식이 포함되어 있습니다.
이를 유지하며 깔끔한 문서로 정리해주세요:

- 제목과 소제목 포함
- 수식은 그대로 유지
- 항목은 리스트로
- 중복 표현과 오타는 자연스럽게 정리

텍스트:
{text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 수식 포함 문서를 정리하는 조교야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    print("✅ GPT 요약 완료")
    return response["choices"][0]["message"]["content"]

def save_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 저장 완료: {path}")

def convert_md_to_pdf(md_path, pdf_path):
    subprocess.run(["pandoc", md_path, "-o", pdf_path], check=True)
    print(f"✅ PDF 변환 완료: {pdf_path}")

if __name__ == "__main__":
    merged_pdf_path = os.path.join(output_folder, merged_pdf_name)
    text_path = os.path.join(output_folder, text_file)
    md_path = os.path.join(output_folder, markdown_file)
    final_pdf_path = os.path.join(output_folder, pdf_file)

    print("📦 1. PDF 병합 중...")
    merged = merge_pdfs(input_folder, merged_pdf_path)
    if not merged:
        exit()

    print("🔍 2. 텍스트 추출 중...")
    extracted = extract_text_with_plumber(merged)
    latexified = wrap_latex_equations(extracted)
    save_file(text_path, latexified)

    print("🤖 3. GPT 요약 중...")
    markdown = summarize_with_gpt(latexified)
    save_file(md_path, markdown)

    print("📝 4. Markdown → PDF 변환 중...")
    convert_md_to_pdf(md_path, final_pdf_path)

    print("🎉 전체 자동화 완료!")
