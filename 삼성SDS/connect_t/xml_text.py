import json
import os
import re
import xml.etree.ElementTree as ET
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

def extract_text_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    extracted_data = []

    # 'name' 태그의 텍스트를 모두 추출합니다.
    for element in root.iter('name'):
        if element.text and element.text.strip():
            # '<SEP>' 문자열을 제거하고, 텍스트를 리스트에 추가
            cleaned_text = element.text.replace('<SEP>', '').strip()
            extracted_data.append(cleaned_text)

    # 추출된 텍스트들을 줄바꿈(\n)으로 연결
    return "\n".join(extracted_data)

def get_page_number_from_filename(filename): #각 xml 파일의 번호를 페이지 번호로 지정함
    match = re.search(r'\d+', filename)
    if match:
        return match.group()
    return 'unknown'

def process_xml_files(file_paths):
    all_text_data = []

    for file_path in file_paths:
        filename = os.path.basename(file_path)
        text = extract_text_from_xml(file_path)
        if text:  # 텍스트가 비어 있지 않을 때만 추가
            page_number = get_page_number_from_filename(filename)
            all_text_data.append({
                'page': page_number,
                'text': text
            })

    return all_text_data

def save_text_to_json(text_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(text_data, file, ensure_ascii=False, indent=4)

# Tkinter를 사용하여 파일 선택 대화상자를 엽니다.
def select_files():
    Tk().withdraw()  # Tkinter 윈도우를 숨깁니다.
    file_paths = askopenfilenames(title="Select XML files", filetypes=[("XML files", "*.xml")])
    return file_paths

# 파일 선택 대화상자를 통해 XML 파일들을 선택합니다.
selected_files = select_files()

if selected_files:
    # XML 파일들을 처리하고 텍스트를 추출하여 저장합니다.
    extracted_text_data = process_xml_files(selected_files)

    # 결과를 저장할 JSON 파일 경로 설정 <-- 이 부분은 경로 변경하시면 됩니다.
    output_file = '../temp/116382275.json'

    save_text_to_json(extracted_text_data, output_file)
    print(f'Text has been extracted and saved to {output_file}')
else:
    print("No files were selected.")
