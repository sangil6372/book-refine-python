import os
import shutil
import fitz  # PyMuPDF
from pdfminer.layout import LTImage, LTContainer, LTPage, LTTextBox, LTTextLine, LAParams
from pdfminer.image import ImageWriter
from pdfminer.high_level import extract_pages
import tkinter as tk
from tkinter import filedialog

def get_image(layout_object):
    if isinstance(layout_object, LTImage):
        return layout_object
    if isinstance(layout_object, LTContainer):
        for child in layout_object:
            return get_image(child)
    else:
        return None

def get_text(layout_object):
    text_content = []
    if isinstance(layout_object, (LTTextBox, LTTextLine)):
        text_content.append(layout_object.get_text())
    if isinstance(layout_object, LTContainer):
        for child in layout_object:
            text_content.extend(get_text(child))
    return text_content

def save_images_from_page(page: LTPage, out_path):
    images = list(filter(bool, map(get_image, page)))
    image_info = []
    for image in images:
        bbox = image.bbox
        # Create a custom filename
        iw = ImageWriter(out_path)
        iw.export_image(image)
        image_info.append({
            'name': image.name,
            'bbox': bbox
        })
    return image_info

# Tkinter를 사용하여 PDF 파일 선택
root = tk.Tk()
root.withdraw()  # Tkinter 윈도우 숨기기
pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

if pdf_path:
    # PDF 파일 열기
    doc = fitz.open(pdf_path)
    laparams = LAParams(detect_vertical=True, all_texts=True)
    pages = list(extract_pages(pdf_path, laparams=laparams))

    # 이미지 저장 경로 설정
    out_path = 'output_dir'
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    page_text = {}

    for page_number, page in enumerate(pages):
        doc_page = doc.load_page(page_number)
        image_info = save_images_from_page(page, out_path)
        page_text[page_number] = doc_page.get_text()

        for info in image_info:
            bbox_str = "_".join(map(str, map(int, info['bbox'])))
            shutil.move(os.path.join(out_path, f"{info['name']}.jpg"), os.path.join(out_path, f"{page_number}page_{bbox_str}.jpg"))

    # 텍스트 저장 경로 설정 및 파일 저장
    text_output_path = os.path.join(out_path, "extracted_text.txt")
    with open(text_output_path, "w", encoding="utf-8") as text_file:
        for page_num, text in page_text.items():
            text_file.write(f"Page {page_num + 1}\n")
            text_file.write(text)
            text_file.write("\n\n")

    print(f"Images and text have been saved to '{out_path}'")
    print(f"Extracted text saved to '{text_output_path}'")
else:
    print("No PDF file selected")
