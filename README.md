# 📘 PDF 자동 요약 정리 시스템 (GPT + Pandoc 기반)

이 프로젝트는 PDF 파일들을 병합하고, 텍스트를 추출한 후 GPT-4를 활용해 개념 설명과 수식 풀이가 포함된 학습 문서로 요약 정리한 뒤, HTML 형식으로 출력하는 자동화 파이프라인입니다.

---

## ✅ 주요 기능

- `upload/` 폴더 내 PDF 파일 병합
- PDF 내 텍스트 및 수식 추출
- 수식은 자동으로 `$...$` 형태로 감싸 LaTeX 처리
- GPT-4로 문서 요약 및 개념 설명 자동화
- 결과를 마크다운(`.md`) 및 HTML로 출력
- API 키는 `.env` 파일로 안전하게 관리

---

## 📁 폴더 구조

````

project/
├── main.py             # 전체 실행 스크립트
├── config.py           # GPT 클라이언트 생성 (API 키 숨김)
├── .env                # OpenAI API 키 저장 (깃허브에 올리지 않음)
├── .gitignore          # .env 제외 설정
├── upload/             # 원본 PDF 파일 저장 폴더
└── result/             # 병합 및 출력 결과 저장 폴더
├── merged.pdf
├── extracted\_text.txt
├── summary.md
└── summary.html

````

---

## ⚙️ 설치 방법

### 1. 필수 라이브러리 설치

```bash
pip install openai python-dotenv pdfplumber PyPDF2
````

### 2. Pandoc 설치 (HTML 변환용)

* [https://pandoc.org/install.html](https://pandoc.org/install.html)
* Windows: `choco install pandoc` (관리자 CMD)
* 설치 확인: `pandoc --version`

---

## 🔐 API 키 설정

`.env` 파일을 프로젝트 루트에 생성하고 다음과 같이 작성:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ `.env`는 반드시 `.gitignore`에 등록되어 있어야 합니다.

---

## ▶️ 실행 방법

```
python main.py
```

실행 후 다음 파일들이 생성됩니다:

* `result/merged.pdf` : 병합된 PDF
* `result/extracted_text.txt` : 원문 텍스트 (수식 포함)
* `result/summary.md` : GPT 요약 문서
* `result/summary.html` : 최종 학습 문서 (브라우저에서 열기 가능)

---

## 💡 요약 문서 특징

* **모든 설명은 한국어**
* 수식은 `$...$`로 표기되어 HTML 내에서 수식처럼 렌더링 가능
* 각 개념에 대해 쉬운 한국어 설명이 자동 추가됨
* 문서 끝에 "질문 유도 문장" 없이 자연스럽게 마무리됨

---

## 🧠 향후 확장 아이디어

* MathJax 템플릿 자동 포함 (HTML에서 수식 실제 렌더링)
* PDF 최종 출력 (LaTeX 엔진 있는 경우)
* 퀴즈/예제 자동 생성 기능 추가
* GUI 실행 도구 (`Tkinter`, `PyQt`)
