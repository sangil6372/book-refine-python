from pdf2image import convert_from_path
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def pdf_to_png(pdf_path, output_base_folder, dpi=300):  # DPI를 600으로 설정하여 고해상도 이미지 생성
    # PDF 파일 이름 추출 (확장자 제외)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # 출력 폴더 경로 생성
    output_folder = os.path.join(output_base_folder, pdf_name)

    # PDF를 이미지로 변환
    images = convert_from_path(pdf_path, dpi=dpi)

    # 출력 폴더가 존재하지 않으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 변환된 이미지를 파일로 저장
    for i, image in enumerate(images):
        output_path = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(output_path, 'PNG', quality=100)
        print(f"Saved: {output_path}")

# PDF 파일 선택
def select_pdf_file():
    root = Tk()
    root.withdraw()  # Tkinter 창 숨기기
    file_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
    root.destroy()
    return file_path

# PDF 파일 경로와 출력 기본 폴더 경로 설정
pdf_path = select_pdf_file()
output_base_folder = r'C:\Users\USER\Desktop\png_folder'

# PDF를 PNG로 변환하여 저장
if pdf_path:
    pdf_to_png(pdf_path, output_base_folder)
else:
    print("PDF 파일을 선택하지 않았습니다.")
