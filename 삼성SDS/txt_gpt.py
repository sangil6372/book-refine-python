import base64

from openai import OpenAI
import os
import tkinter as tk
from tkinter import filedialog

MODEL: str = 'gpt-4o'
client: OpenAI = OpenAI(api_key=os.getenv('OPENAI_API_KEY', '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'))

# 1. json 파일 불러옴
# 2. json 리스트 순회하면서 각 json 의 page , text 가져옴

def encode_image(image_path):
  with open(image_path, 'rb') as image_path:
    return base64.b64encode(image_path.read()).decode('utf-8')

image_path = r"C:\Users\USER\Desktop\삼성SDS\png_folder\170374564\image_12.png"

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": ""},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/png;base64,{encode_image(image_path)}"
          },
        },
      ],
    }
  ],
  max_tokens=1000,
)

print(response.choices[0].message.content)
