import io
import ebooklib
from ebooklib import epub
from PIL import Image
from bs4 import BeautifulSoup
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import warnings

# 경고 메시지 숨기기
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def epub_to_png(epub_path, output_base_folder, dpi=300):
    # EPUB 파일 이름 추출 (확장자 제외)
    epub_name = os.path.splitext(os.path.basename(epub_path))[0]

    # 출력 폴더 경로 생성
    output_folder = os.path.join(output_base_folder, epub_name)

    # EPUB을 열기
    book = epub.read_epub(epub_path)

    # 출력 폴더가 존재하지 않으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 커버 이미지 추출 및 저장
    cover_image_found = False
    for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        if 'cover' in item.file_name.lower():
            cover_image_data = item.get_content()
            cover_image = Image.open(io.BytesIO(cover_image_data))
            cover_output_path = os.path.join(output_folder, 'cover.png')
            cover_image.save(cover_output_path, 'PNG', quality=100)
            print(f"Saved: {cover_output_path}")
            cover_image_found = True
            break

    if not cover_image_found:
        print("Cover image not found.")

    # 이미지 파일의 순서를 저장할 리스트
    image_items = []

    # HTML 파일을 파싱하여 이미지 순서 추출
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')
        for img in soup.find_all('img'):
            # 이미지 경로 추출
            img_src = img.get('src')
            # 이미지 경로 정규화
            img_src = os.path.basename(img_src)
            for image_item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
                if image_item.file_name.endswith(img_src):
                    image_items.append(image_item)
                    break

    # 커버 이미지가 image_items에 있으면 제거
    image_items = [item for item in image_items if 'cover' not in item.file_name.lower()]

    # 나머지 이미지 추출 및 저장
    for i, item in enumerate(image_items):
        image_data = item.get_content()
        image = Image.open(io.BytesIO(image_data))
        output_path = os.path.join(output_folder, f"image_{i + 1}.png")
        image.save(output_path, 'PNG', quality=100)
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
output_base_folder = r'C:\Users\USER\Desktop\삼성SDS\png_folder'

# EPUB를 PNG로 변환하여 저장
if epub_path:
    epub_to_png(epub_path, output_base_folder)
else:
    print("EPUB 파일을 선택하지 않았습니다.")
