import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from hanspell import spell_checker
from hanspell.constants import CheckResult

# Tesseract OCR 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'




class PDFTextExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Text Extractor")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None
        self.start_x = None
        self.start_y = None

        self.pdf_path = None
        self.page_image = None
        self.current_page = 0
        self.document = None

        self.load_pdf_button = tk.Button(root, text="Load PDF", command=self.load_pdf)
        self.load_pdf_button.pack(side=tk.LEFT)

        self.prev_button = tk.Button(root, text="Previous Page", command=self.show_prev_page)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(root, text="Next Page", command=self.show_next_page)
        self.next_button.pack(side=tk.LEFT)

    def load_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            self.document = fitz.open(self.pdf_path)
            self.current_page = 0
            self.show_page(self.current_page)

    def show_page(self, page_num):
        if self.document is None:
            return
        if page_num < 0 or page_num >= len(self.document):
            return

        page = self.document.load_page(page_num)
        pix = page.get_pixmap()
        self.page_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        self.tk_image = ImageTk.PhotoImage(self.page_image)

        # 캔버스 크기를 PDF 페이지 크기와 맞추기
        self.canvas.config(width=pix.width, height=pix.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def show_next_page(self):
        if self.document and self.current_page < len(self.document) - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def show_prev_page(self):
        if self.document and self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        bbox = (self.start_x, self.start_y, end_x, end_y)
        self.extract_text_from_bbox(bbox)

    def extract_text_from_bbox(self, bbox):
        if not self.page_image:
            return

        cropped_image = self.page_image.crop(bbox)

        # 이미지 사전 처리
        cropped_image_cv = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cropped_image_cv, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        processed_image = Image.fromarray(binary_image)
        custom_config = r'--oem 3 --psm 6'  # 기본 엔진 및 신경망 기반 엔진 사용, 단일 유니폼 블록의 텍스트 가정
        text = pytesseract.image_to_string(processed_image, lang='kor', config=custom_config)

        spelled_text = spell_checker.check(text)
        print("Extracted Text:", spelled_text)
        checked_text = spelled_text.checked
        print(checked_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFTextExtractor(root)
    root.mainloop()
