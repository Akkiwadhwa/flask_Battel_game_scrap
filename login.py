import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def login(username,password):
    url = "https://www.baseattackforce.com/"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('window-size=1050x708')
    options.add_experimental_option("detach", True)
    driver1 = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver1.get(url)
    driver1.find_element(By.ID,"loginname").send_keys(username)
    driver1.find_element(By.ID, "loginpass").send_keys(password)
    driver1.find_element(By.ID,"bigbutton").click()
    print("Please wait while loging in.")
    time.sleep(5)
    return driver1

