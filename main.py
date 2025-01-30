import msvcrt
import time
import pyautogui
import pytesseract
from PIL import Image
import re
import os

# Tesseract OCR 경로 설정 (설치된 경로에 맞게 수정 필요)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_and_execute(image_url, callback):
    """
    화면에서 특정 이미지를 찾고 callback 함수를 실행하는 함수
    
    Args:
        image_url (str): 찾고자 하는 이미지의 URL
        callback (callable): 이미지를 찾았을 때 실행할 콜백 함수
                           콜백 함수는 위치 정보(x, y)를 인자로 받음
    """
    try:
        # 화면에서 이미지 찾기
        location = pyautogui.locateOnScreen(os.path.abspath(image_url))
        
        if location:
            # 이미지의 중앙 좌표 계산
            center_x = location.left + location.width / 2
            center_y = location.top + location.height / 2
            
            print(f"이미지를 찾았습니다: 위치 ({center_x}, {center_y})")
            
            # 콜백 함수 실행
            callback(center_x, center_y)
            return True
        else:
            print("이미지를 찾을 수 없습니다.")
            return False
            
    except Exception as e:
        print(f"이미지 검색 중 오류 발생: {e}")
        return False
    
def capture_and_read_numbers(region):
    """
    지정된 영역의 스크린샷을 찍고 숫자를 읽어오는 함수
    region: (x, y, width, height) 형식의 튜플
    """
    try:
        # 지정된 영역의 스크린샷 촬영
        screenshot = pyautogui.screenshot(region=region)
        
        # OCR 수행 (숫자만 추출)
        text = pytesseract.image_to_string(screenshot, config='--psm 6 outputbase digits')
        
        # 숫자만 추출
        numbers = re.findall(r'\d+', text)
        
        return numbers[0] if numbers else None
    
    except Exception as e:
        print(f"숫자 인식 중 오류 발생: {e}")
        return None

print("프로그램을 종료하려면 ESC 키를 누르세요.")
print("지정된 영역의 숫자를 읽어오려면 R 키를 누르세요.")

# 숫자를 읽어올 화면 영역 설정 (예시 값)
target_region = (100, 100, 200, 50)  # (x, y, width, height)

def after_timeout(fn):
    time.sleep(3)
    if fn is not None:
      fn()

def click(x, y, fn):
    print('move & click')
    pyautogui.moveTo(x,y)
    pyautogui.click()

    if fn is not None:
      fn()

def auto_afk_battle():
    find_and_execute('./res/auto-battle.png', lambda x, y: click(x, y, None))

def auto_afk_failed():
    find_and_execute('./res/retry.png', lambda x, y: click(x,y, after_timeout(auto_afk_battle)))

# main
try:
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # ESC
                print("\n프로그램을 종료합니다.")
                break
            
        auto_afk_failed()
        auto_afk_battle()
        
        print("---")
        time.sleep(3)
except KeyboardInterrupt:
    print("\n프로그램이 중단되었습니다.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")