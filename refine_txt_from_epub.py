import warnings

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=UserWarning, module='ebooklib')
warnings.filterwarnings("ignore", category=FutureWarning, module='ebooklib')

def epub_to_text(epub_path, output_base_folder):
    # EPUB 파일 이름 추출 (확장자 제외)
    epub_name = os.path.splitext(os.path.basename(epub_path))[0]

    # 출력 폴더 경로 생성
    output_folder = os.path.join(output_base_folder, epub_name)

    # EPUB을 열기
    book = epub.read_epub(epub_path)

    # 출력 폴더가 존재하지 않으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 텍스트 추출 및 저장
    full_text = ""
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')
        text = soup.get_text(separator='\n')
        full_text += text + '\n\n'

    # 텍스트 파일로 저장
    output_path = os.path.join(output_folder, f"{epub_name}.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
        print(f"Saved: {output_path}")

# EPUB 파일 선택
def select_epub_file():
    root = Tk()
    root.withdraw()  # Tkinter 창 숨기기
    file_path = askopenfilename(filetypes=[("EPUB files", "*.epub")])
    root.destroy()
    return file_path

# EPUB 파일 경로와 출력 기본 폴더 경로 설정
epub_path = select_epub_file()
output_base_folder = r'C:\Users\USER\Desktop\삼성SDS\text_folder'

# EPUB에서 텍스트를 추출하여 저장
if epub_path:
    epub_to_text(epub_path, output_base_folder)
else:
    print("EPUB 파일을 선택하지 않았습니다.")
