import pyautogui
import time
import keyboard

# 몇 번 스크롤할지 설정
scroll_count = 10000  # 스크롤 횟수
scroll_interval = 0.5   # 스크롤 간격 (초)
paused = False  # 스크롤 일시정지 여부

def toggle_pause():
    global paused
    paused = not paused

keyboard.add_hotkey('esc', toggle_pause)  # esc 키를 누르면 일시정지 또는 재개

for _ in range(scroll_count):
    if paused:
        while paused:
            time.sleep(0.1)  # 일시 정지 상태에서 대기 (CPU 과부하 방지)
    pyautogui.scroll(-5)  # 마우스를 아래로 스크롤
    time.sleep(scroll_interval)  # n초 대기 