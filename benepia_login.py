import os
import sys
import json
import stat
import time
import psutil
import zipfile
import shutil
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# 실행 위치 기준 경로 처리 (PyInstaller 호환)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "benepia_config.json")
CHROMEDRIVER_PATH = os.path.join(BASE_DIR, "chromedriver.exe")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# config 로딩
if not os.path.exists(CONFIG_PATH):
    print("❗ benepia_config.json 파일이 없습니다.")
    sys.exit(1)

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

ID = config["ID"]
PASSWD = config["PASSWD"]
LOGIN_URL = config["LOGIN_URL"]

# 삭제 오류 대응
def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# 크롬 드라이버 버전 확인
def get_local_driver_version():
    try:
        result = os.popen(f'"{CHROMEDRIVER_PATH}" --version').read()
        version = result.strip().split(" ")[1]
        return version
    except Exception:
        return None

# 최신 버전 크롤링
def get_latest_driver_version():
    url = "https://googlechromelabs.github.io/chrome-for-testing/"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    stable_section = soup.find('a', {'href': '#stable'})
    code_tag = soup.find('td').find('code').text
    return code_tag

# 최신 드라이버 다운로드
def update_driver(latest_version):
    os.makedirs(TEMP_DIR, exist_ok=True)
    zip_url = f"https://storage.googleapis.com/chrome-for-testing-public/{latest_version}/win64/chromedriver-win64.zip"
    zip_path = os.path.join(TEMP_DIR, "chromedriver-win64.zip")

    print(f"⬇️ 최신 크롬 드라이버 다운로드 중: {latest_version}")
    with requests.get(zip_url, stream=True) as r:
        r.raise_for_status()
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(TEMP_DIR)

    src_path = os.path.join(TEMP_DIR, "chromedriver-win64", "chromedriver.exe")
    shutil.move(src_path, CHROMEDRIVER_PATH)
    print(f"✅ 드라이버 업데이트 완료 → {CHROMEDRIVER_PATH}")
    shutil.rmtree(TEMP_DIR, onerror=remove_readonly)

# OneDrive 실행 중인지 확인 (출력용)
def is_onedrive_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'OneDrive.exe' in proc.info['name']:
            return True
    return False

# 크롬 자동화 시작
def login():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=chrome_options)
    driver.get(LOGIN_URL)
    driver.implicitly_wait(2)

    driver.find_element(By.CLASS_NAME, 'execu_log_input_id').send_keys(ID)
    driver.find_element(By.CLASS_NAME, 'execu_log_input_pw').send_keys(PASSWD)

    # 로그인 버튼 기다렸다가 클릭 (수정된 구조 반영)
    wait = WebDriverWait(driver, 10)
    login_button = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, ".login_btn_controls a"
    )))
    login_button.click()

# 실행 순서
if __name__ == "__main__":
    print("🔍 크롬 드라이버 버전 확인 중...")
    local_version = get_local_driver_version()
    latest_version = get_latest_driver_version()

    if local_version != latest_version:
        print(f"⚠️ 드라이버 업데이트 필요: {local_version} → {latest_version}")
        update_driver(latest_version)
    else:
        print(f"✅ 최신 드라이버 사용 중: {local_version}")

    if is_onedrive_running():
        print("ℹ️ OneDrive 실행 중입니다.")

    print("🚀 자동 로그인 시작...")
    try:
        login()
    except WebDriverException as e:
        print("❌ 로그인 실패:", str(e))
