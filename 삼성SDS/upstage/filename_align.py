import json
import re

# JSON 파일의 경로를 설정 (예: 'input.json')
input_file_path = '마술펑.json'

# JSON 파일 읽기 (UTF-8 인코딩 지정)
with open(input_file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# 정렬을 위한 함수 정의
def sort_key(item):
    # 'filename' 속성에서 숫자를 추출하기 위한 정규식
    match = re.search(r'page_(\d+)\.png', item['filename'])
    if match:
        return int(match.group(1))
    return 0  # 만약 숫자를 찾을 수 없다면 기본값을 0으로 반환

# filename 속성 기준으로 정렬
json_data_sorted = sorted(json_data, key=sort_key)

# 수정된 데이터를 저장할 파일 경로 설정 (예: 'sorted_output.json')
output_file_path = 'sorted_output.json'

# 수정된 JSON 데이터를 파일에 저장 (UTF-8 인코딩으로 저장)
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(json_data_sorted, file, indent=4)

print(f"Sorted JSON data has been saved to {output_file_path}")
