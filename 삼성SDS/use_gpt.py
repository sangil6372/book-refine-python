import os
import tkinter as tk
from tkinter import filedialog
import json
from openai import OpenAI
import base64
from dotenv import load_dotenv

load_dotenv()

MODEL: str = 'gpt-4o-mini'
client: OpenAI = OpenAI(api_key=os.getenv("GPT_API_KEY"))


# 파일 탐색기를 사용하여 파일을 선택하는 함수
def select_file(file_type, file_extensions, dialog_title):
    root = tk.Tk()
    root.withdraw()  # Tkinter 윈도우를 숨김
    file_path = filedialog.askopenfilename(
        title=dialog_title,
        filetypes=[(file_type, file_extensions)]
    )
    return file_path

flag = 0


# 이미지 파일을 base64로 인코딩하는 함수
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# 파일 선택
image_folder_path = filedialog.askdirectory(title="이미지 폴더를 선택하세요")
json_file_path = select_file("JSON Files", "*.json", "OCR 텍스트가 저장된 JSON 파일을 선택하세요")

# JSON 파일 읽기
if json_file_path:
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        extracted_data = json.load(json_file)
else:
    print("JSON 파일을 선택하지 않았습니다.")
    exit()

# GPT API를 사용한 오타 검증 함수
def check_image_and_text_with_gpt(image_file_path, text):
    try:
        image_base64 = encode_image(image_file_path)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "당신은 이미지에서 추출한 한국어 텍스트를 검수하는 도우미입니다."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": f"첨부된 이미지는 호시다 타다히코가 지은 '단위의 사전' 도서의 이미지입니다. 이미지 에서 텍스트를 읽고서 OCR로 추출된 한국어 텍스트가 제대로 추출되었는지 교차로 검수해주세요, 텍스트 추출에 오류가 있거나 맞춤법이 틀렸을 경우 수정해 주세요. 답변은 부가 정보 없이 수정된 텍스트 그대로 건네주세요. 다음은 추출된 텍스트입니다. : \n\n{text}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=3000
        )

        # # 응답을 출력하여 확인
        # if flag == 0:
        #     print(response)

        corrected_text = response.choices[0].message.content.strip()

        print(corrected_text)

        return corrected_text

    except Exception as e:
        print(f"An error occurred during API call: {e}")
        return None


# 이미지 폴더 순회 및 오타 검증
try:
    for image_filename in os.listdir(image_folder_path):
        if image_filename.endswith(".png"):
            image_number = str(int(image_filename.split('_')[1].split('.')[0]))  # 페이지 번호를 문자열로 변환

            # 해당 이미지 번호의 OCR 텍스트 추출
            ocr_text_entry = next((entry for entry in extracted_data if entry['page'] == image_number), None)

            print(image_number)

            if ocr_text_entry is not None:
                ocr_text = ocr_text_entry['text']

                # if flag == 0:
                #     print(ocr_text, flush=True)
                #     flag = 1

                image_path = os.path.join(image_folder_path, image_filename)

                # GPT API로 이미지와 텍스트 검증
                corrected_text = check_image_and_text_with_gpt(image_path, ocr_text)

                # 결과를 업데이트
                ocr_text_entry['text'] = corrected_text
            else:
                print(f"이미지 {image_number}에 해당하는 OCR 텍스트가 JSON 파일에서 발견되지 않았습니다.", flush=True)
except Exception as e:
    print(f"An error occurred: {e}", flush=True)

# 수정된 데이터를 새 JSON 파일로 저장
root = tk.Tk()
root.withdraw()  # Tkinter 윈도우를 숨김
output_json_file_path = filedialog.asksaveasfilename(
    title="업데이트된 JSON 파일을 저장할 위치를 선택하세요",
    defaultextension=".json",
    filetypes=[("JSON Files", "*.json")]
)

if output_json_file_path:
    with open(output_json_file_path, 'w', encoding='utf-8') as output_json_file:
        json.dump(extracted_data, output_json_file, ensure_ascii=False, indent=4)
    print(f"오타 검증이 완료되었으며, 결과가 {output_json_file_path} 파일에 저장되었습니다.", flush=True)
else:
    print("저장 경로가 선택되지 않았습니다.", flush=True)
