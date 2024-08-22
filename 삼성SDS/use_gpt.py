from openai import OpenAI
import os
import tkinter as tk
from tkinter import filedialog

MODEL: str = 'gpt-4o'
client: OpenAI = OpenAI(api_key=os.getenv('OPENAI_API_KEY', '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'))

# check

# 파일 탐색기를 사용하여 이미지 파일을 선택하는 함수
def select_image_file():
    root = tk.Tk()
    root.withdraw()  # Tkinter 윈도우를 숨김
    file_path = filedialog.askopenfilename(
        title="이미지 파일을 선택하세요",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    return file_path

# 이미지 파일 선택
image_path = select_image_file()

# 이미지를 읽고, 해당 이미지를 GPT-4에게 주면서 요청을 만듭니다.
if image_path:
    with open(image_path, 'rb') as image_file:
        completion = client.chat.completions.create(
            model= MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": ""},

            ]
        )

    # GPT의 응답을 텍스트 파일로 저장
    with open('extracted_text.txt', 'w') as text_file:
        text_file.write(completion.choices[0].message['content'])
else:
    print("이미지 파일을 선택하지 않았습니다.")