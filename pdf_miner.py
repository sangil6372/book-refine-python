import os
import json
import fitz  # PyMuPDF
from tkinter import filedialog
import tkinter as tk

# Tkinter를 사용하여 PDF 파일 선택
root = tk.Tk()
root.withdraw()  # Tkinter 윈도우 숨기기
pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

if pdf_path:
    # PDF 파일 이름에서 확장자를 제거하고 그 이름을 사용하여 JSON 파일을 저장
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]

    # PDF 파일 열기
    doc = fitz.open(pdf_path)

    # 페이지별로 텍스트 추출
    page_texts = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        page_texts.append({"page": page_num + 1, "text": text})

    # JSON 출력 경로 설정
    output_dir = 'json_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, f'{pdf_filename}.json')

    # JSON 파일로 저장
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(page_texts, json_file, ensure_ascii=False, indent=4)

    print(f"Text extracted and saved to '{output_path}'")
else:
    print("No PDF file selected")