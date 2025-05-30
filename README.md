# 📄 PDF 병합 프로그램 - `main.py`

이 프로그램은 `upload/` 폴더에 업로드된 여러 개의 PDF 파일을 **이름 순으로 정렬하여 병합**하고, 결과물을 `result/` 폴더에 `merged.pdf`라는 이름으로 저장합니다.

---

## 📁 폴더 구조

```
project/
├── main.py              # 병합 기능을 수행하는 메인 파이썬 파일
├── upload/              # 병합할 PDF 파일들을 넣는 폴더
│   ├── a.pdf
│   ├── b.pdf
│   └── ...
└── result/              # 병합된 PDF가 저장될 폴더
    └── merged.pdf
```

---

## ⚙️ 사용 방법  

1. `upload/` 폴더에 병합하고 싶은 `.pdf` 파일들을 넣습니다.  
2. 터미널 또는 명령 프롬프트에서 `main.py`를 실행합니다:  

   ```
   python main.py
   ```
3. 병합된 결과는 `result/merged.pdf`로 저장됩니다.  

---

## 🧠 주요 기능 설명  

* **PDF 정렬**: 파일 이름 기준으로 오름차순 정렬  
* **자동 폴더 생성**: `upload/`, `result/` 폴더가 없다면 자동 생성  
* **에러 처리**: PDF가 없을 경우 안내 메시지 출력  

---

## 🧪 사용 예시

### 예시 입력

`upload/` 폴더에 다음과 같은 PDF가 있을 경우:  

```
01_intro.pdf
02_content.pdf
03_summary.pdf
```

### 실행 결과

`result/merged.pdf`는 위 파일 순서대로 병합된 하나의 PDF 파일입니다.  

---

## 🐍 사용된 주요 라이브러리

* [`PyPDF2`](https://pypi.org/project/PyPDF2/)  
  PDF 병합에 사용되는 파이썬 라이브러리  

설치 명령어:  

```
pip install PyPDF2
pip install pdfplumber
```

---

## 🛠 코드 주요 부분 요약

```
pdf_files = sorted([
    f for f in os.listdir(input_folder)
    if f.lower().endswith('.pdf')
])
```

* `upload/` 폴더에서 PDF 파일을 읽고 이름순으로 정렬  

```
merger = PdfMerger()
for pdf in pdf_files:
    merger.append(os.path.join(input_folder, pdf))
```

* 정렬된 순서로 PDF 병합  

```
merger.write(output_path)
merger.close()
```

* 결과물을 `result/merged.pdf`로 저장하고 종료  

---

## 📌 주의사항  

* 프로그램 실행 위치는 반드시 `main.py`가 위치한 폴더여야 합니다.  
* PDF 확장자는 `.PDF`, `.Pdf` 등 대소문자 구분 없이 인식됩니다.  
* 파일명이 한글일 경우 운영체제 인코딩 문제로 병합 실패할 수 있으니 주의하세요.  
