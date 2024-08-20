import json

# JSON 파일의 경로를 설정 (파일을 직접 사용할 경우, 경로를 입력하세요)
input_file_path = 'sorted_output.json'  # 예: 'C:\\path\\to\\your\\file.json'

# JSON 파일 읽기 (UTF-8 인코딩 지정)
with open(input_file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# billed_pages 값을 1부터 증가시키기 위한 변수 초기화
page_counter = 1

# 데이터 처리
for item in json_data:
    if 'billed_pages' in item:
        item['billed_pages'] = page_counter
        page_counter += 1

    # 내부의 response 객체에서 billed_pages 업데이트
    if 'response' in item and 'billed_pages' in item['response']:
        item['response']['billed_pages'] = page_counter
        page_counter += 1

# 수정된 데이터를 저장할 파일 경로 설정
output_file_path = '../upstage_result/88918752.json'  # 예: 'C:\\path\\to\\your\\updated_file.json'

# 수정된 JSON 데이터를 파일에 저장 (UTF-8 인코딩으로 저장)
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(json_data, file, indent=4, ensure_ascii=False)

print(f"Updated JSON data has been saved to {output_file_path}")
