import pandas as pd
import tkinter as tk
from tkinter import filedialog
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# 인프라넷에서 다운로드 한 엑셀 파일을 업로드
# 시트에서 작업자명을 가져와 엑셀 파일과 병합하여 업데이트 하는 코드입니다.


# Google 스프레드시트에서 데이터를 가져오는 함수
def get_data_from_google_sheets(spreadsheet_url, worksheet_name):
    # Google Sheets API에 접근하기 위한 범위 설정
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # 자격 증명 파일 경로 (개인에 맞게 수정 필요)
    json_key_path = r'C:\Users\USER\PycharmProjects\pythonProject1\웅진북센\작업자관리\fiery-catwalk-434403-c2-89fd46213af3.json'

    # 자격 증명 파일을 통해 인증
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
    client = gspread.authorize(credentials)

    # 스프레드시트를 URL로 열기
    spreadsheet = client.open_by_url(spreadsheet_url)

    # 워크시트 열기
    worksheet = spreadsheet.worksheet(worksheet_name)

    # 시트의 데이터를 모두 가져오기
    data = worksheet.get_all_records()

    # 데이터프레임으로 변환
    df = pd.DataFrame(data)

    return df, worksheet


# Google 스프레드시트에 데이터를 한 번에 업로드하는 함수
def upload_dataframe_to_google_sheets(df, worksheet):
    # 스프레드시트의 기존 데이터를 삭제
    worksheet.clear()

    # DataFrame을 리스트로 변환
    data = [df.columns.values.tolist()] + df.values.tolist()  # 헤더 포함

    # 스프레드시트 범위에 데이터를 한 번에 업로드
    worksheet.update(range_name='A1', values=data)  # A1 셀부터 데이터 전체 업로드


# Tkinter 초기화
root = tk.Tk()
root.withdraw()  # Tkinter 창 숨기기

# 파일 선택 창 띄우기 (엑셀 파일 선택)
file_path = filedialog.askopenfilename(
    title="엑셀 파일을 선택하세요",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

# 선택한 엑셀 파일 불러오기 (엑셀 파일에 닉네임과 데이터가 있다고 가정)
df_new = pd.read_excel(file_path)

# 엑셀 데이터 로드 후 컬럼명 확인
print("엑셀에서 불러온 데이터 컬럼:", df_new.columns)

# 'pmadmin162'와 'sangil' 코드네임 제거
df_new = df_new[~df_new['코드네임'].isin(['pmadmin162', 'sangil'])]

df_new.columns = ['닉네임', '제출 날짜', '작업 수량', '표 제출 수', '이미지 제출 수 2', '수식 수량', '텍스트 제출 수', '각주 제출 수', '참고문헌 제출 수']

# '이미지 제출 수 2', '텍스트 제출 수', '각주 제출 수', '참고문헌 제출 수' 열 삭제
df_agg = df_new.drop(columns=['이미지 제출 수 2', '텍스트 제출 수', '각주 제출 수', '참고문헌 제출 수', '표 제출 수'])

# '닉네임'으로 그룹화하고 집계 처리:
# - '작업 수량' 등은 각각 합산
# - '제출 날짜'는 가장 최신 값 사용
df_agg = df_new.groupby(['닉네임']).agg({
    '제출 날짜': 'max',  # 최신 날짜 사용
    '작업 수량': 'sum',
    '수식 수량': 'sum',
}).reset_index()

# 그룹화된 데이터 출력
print("그룹화된 데이터 확인:", df_agg.head())

# 구글 스프레드시트에서 기존 작업자명 및 닉네임 데이터 불러오기
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1aKpkoXNAYkweCS_EFbYcjgCS47y85XLeO-Ge7mDeeuU/edit?gid=911524365'  # 스프레드시트 URL로 변경
worksheet_name = 'LaTeX 작업자 현황'  # 워크시트 이름으로 변경
df_existing, worksheet = get_data_from_google_sheets(spreadsheet_url, worksheet_name)

# '닉네임'을 기준으로 기존 데이터와 엑셀 데이터를 병합
df_merged = pd.merge(df_existing, df_agg, on='닉네임', how='left')

# 필요 없는 '_x', '_y' 컬럼 삭제 후 최종 병합된 데이터 사용
df_merged['제출 날짜'] = df_merged['제출 날짜_y']
df_merged['작업 수량'] = df_merged['작업 수량_y']
df_merged['수식 수량'] = df_merged['수식 수량_y']

# 불필요한 컬럼 삭제
df_merged = df_merged.drop(columns=['제출 날짜_x', '작업 수량_x', '수식 수량_x', '제출 날짜_y', '작업 수량_y', '수식 수량_y'])

# 병합된 데이터를 구글 스프레드시트에 업로드
upload_dataframe_to_google_sheets(df_merged, worksheet)

print("Google 스프레드시트가 성공적으로 업데이트되었습니다.")
