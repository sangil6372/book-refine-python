import json
import re


# JSON 파일을 불러와서 정렬하고 새로운 JSON 파일로 저장하는 함수
def sort_json_and_save(input_file, output_file):
    # JSON 파일 불러오기
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # filename에서 숫자를 추출하여 정렬하기 위한 함수
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    # filename 속성의 숫자 기준으로 정렬
    sorted_data = sorted(data, key=lambda x: extract_number(x["filename"]))

    # "page"와 "text" 속성만 포함하는 리스트로 변환
    transformed_data = [{"page": extract_number(item["filename"]), "text": item["response"].get("text", "")} for item in
                        sorted_data]

    # 새로운 JSON 파일로 저장
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(transformed_data, f, ensure_ascii=False, indent=4)

    print(f"Sorted and transformed JSON file saved as {output_file}")


# 사용 예제
input_file = "30664037.json"  # 기존 JSON 파일 경로
output_file = "sorted_responses.json"  # 새로 저장할 JSON 파일 경로
sort_json_and_save(input_file, output_file)
