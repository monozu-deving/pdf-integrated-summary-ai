import os
import re
import pdfplumber
from PyPDF2 import PdfMerger
import subprocess
from config import get_gpt_client

client = get_gpt_client()

# 📁 경로 설정
input_folder = "upload"
output_folder = "result"
merged_pdf = os.path.join(output_folder, "merged.pdf")
text_file = os.path.join(output_folder, "extracted_text.txt")
md_file = os.path.join(output_folder, "summary.md")
html_file = os.path.join(output_folder, "summary.html")

def merge_pdfs(input_folder, output_path):
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdfs = sorted(f for f in os.listdir(input_folder) if f.lower().endswith('.pdf'))

    if not pdfs:
        print("❌ PDF 파일 없음.")
        return None

    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(os.path.join(input_folder, pdf))
    merger.write(output_path)
    merger.close()
    print(f"✅ 병합 완료: {output_path}")
    return output_path

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    print("✅ 텍스트 추출 완료")
    return text

def wrap_latex(text):
    patterns = [
        r'\bE\s*=\s*mc\^?2\b',
        r'\b[a-zA-Z]+\^2\b',
        r'\b\\int.*?dx\b',
        r'\b[a-zA-Z]+\s*=\s*[^ \n]+',
        r'\b\d+\s*\^\s*\d+\b',
        r'\\frac{.*?}{.*?}',
    ]
    for pat in patterns:
        text = re.sub(pat, lambda m: f"${m.group(0)}$", text)
    print("✅ 수식 LaTeX 포맷 완료")
    return text

def summarize_with_gpt(text):
    prompt = f"""다음은 PDF에서 추출한 원시 텍스트입니다. 이 내용을 바탕으로 학습 자료용 문서를 작성해주세요. 다음 기준을 따르세요:

- 텍스트는 모두 한국어로 작성합니다.
- 각 개념이나 정의가 등장하면, 그 개념을 이해하기 쉽게 1~2문장으로 설명을 추가해주세요.
- 수식이 등장하면 그 수식의 의미도 간단히 한국어로 설명해주세요.
- 중요한 정의, 정리, 결론은 **굵게 강조**해 주세요.
- 마크다운 문법을 사용해서 문서 구조를 깔끔하게 만드세요.
- 목록, 수식, 문단을 구분하여 가독성 좋게 정리해주세요.
- 문서의 끝에 "궁금한 점은 질문하세요", "더 알고 싶으면..." 등의 안내 문장은 절대 추가하지 마세요.
- 마지막 문장은 내용의 자연스러운 마무리로 끝나야 하며, 어떤 경우에도 후속 질문을 유도하지 마세요.

텍스트:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "너는 수식 포함 문서를 요약 정리하는 도우미야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    print("✅ GPT 요약 완료")
    return response.choices[0].message.content

def save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 저장 완료: {path}")

def convert_md_to_html(md_path, html_path):
    try:
        subprocess.run(["pandoc", md_path, "-o", html_path], check=True)
        print(f"✅ HTML 변환 완료: {html_path}")
    except FileNotFoundError:
        print("❌ pandoc 실행 파일을 찾을 수 없습니다. pandoc이 설치되어 있는지 확인하세요.")

if __name__ == "__main__":
    print("📦 1. PDF 병합 중...")
    merged = merge_pdfs(input_folder, merged_pdf)
    if not merged:
        exit()

    print("🔍 2. 텍스트 추출 중...")
    text = extract_text(merged)
    latex_text = wrap_latex(text)
    save(text_file, latex_text)

    print("🤖 3. GPT 요약 요청 중...")
    markdown = summarize_with_gpt(latex_text)
    save(md_file, markdown)

    print("🌐 4. Markdown → HTML 변환 중...")
    convert_md_to_html(md_file, html_file)

    print("\n🎉 전체 자동화 완료!")
