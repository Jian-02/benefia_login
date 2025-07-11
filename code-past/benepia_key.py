#Selenium 용
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from SECRET_benepia import *

import psutil
import os

# OneDrive 사용중인지 확인하는 함수
def is_onedrive_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'OneDrive.exe' in proc.info['name']:
            return True
    return False

#------------------------------Selenium을 이용한 제어 ------------------------------#
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

if is_onedrive_running():
    print("OneDrive가 실행 중입니다.")
    onedrive_directory = os.environ['OneDrive']
    directory_code = onedrive_directory + "\바탕 화면\pycode\chromedriver.exe"
    # OneDrive 사용 시
    driver = webdriver.Chrome(directory_code, options=chrome_options)
else:
    print("OneDrive가 실행 중이지 않습니다.")
    driver = webdriver.Chrome(r"C:\Users\Hansol\바탕 화면\pycode\chromedriver.exe", options=chrome_options)

#Selenium_driver로 url 접속
url = "베네피아주소"

id_key = ID
passwd_key = PASSWD

driver.get(url)
driver.implicitly_wait(2)

driver.find_element(By.CLASS_NAME, 'execu_log_input_id').send_keys(id_key)
driver.find_element(By.CLASS_NAME,'execu_log_input_pw').send_keys(passwd_key)

# driver.find_element(By.CLASS_NAME, "login_btn").click()
driver.find_element(By.XPATH, "//*[@id=\"wrapper\"]/div[2]/div[2]/div[1]/fieldset/div[1]/a").click()