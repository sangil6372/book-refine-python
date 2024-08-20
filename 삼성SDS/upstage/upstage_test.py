import requests
import os
import json

api_key = "up_nyh55pvWcPXMASdwmX9ajcIDiLsBh"
# filename = r"C:\Users\USER\Downloads\PDF변환본\30664037.pdf"

url = "https://api.upstage.ai/v1/document-ai/layout-analysis"
headers = {"Authorization": f"Bearer {api_key}"}

combined_responses = []


folder_path = r"C:\Users\USER\Desktop\삼성SDS\png_folder\170374564"  # 여기에 실제 폴더 경로를 넣어주세요.
# 폴더 내 파일들을 순차적으로 처리
for filename in os.listdir(folder_path):
    # 이미지 파일 경로 생성
    file_path = os.path.join(folder_path, filename)

    # 파일이 실제 파일인지 확인
    if os.path.isfile(file_path):
        try:
            # API 요청을 보낼 이미지 파일을 연다
            with open(file_path, "rb") as image_file:
                files = {"document": image_file}

                # API 요청 보내기
                response = requests.post(url, headers=headers, files=files)

                # 응답 처리
                if response.status_code == 200:
                    response_json = response.json()
                    combined_responses.append({
                        "filename": filename,
                        "response": response_json
                    })
                else:
                    print(f"Failed to process {filename}, status code: {response.status_code}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# 합쳐진 JSON 데이터를 파일로 저장
output_file = "upstage_result.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(combined_responses, f, ensure_ascii=False, indent=4)

print(f"Combined JSON file saved as {output_file}")


# files = {"document": open(filename, "rb")}
# response = requests.post(url, headers=headers, files=files)
# print(response.json())