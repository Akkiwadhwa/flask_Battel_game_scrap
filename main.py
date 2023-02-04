import time
import requests
from alliance import alliance
from battles import battles
from members import members
from ranking import ranking
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def login():
    url = "https://www.baseattackforce.com/"
    options = Options()
    options.add_argument("--headless")
    driver1 = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3)
    input("After login, Press enter to continue: ")
    time.sleep(3)
    return driver1


print("Welcome to the scrapper.")
r = requests.get("https://api.ipify.org/").text
print(f"Your i.p is {r}")
print(
    "Please add this i.p  in your remote sql in cpanel --> https://www.nouahsark.com:2083/cpsess9648297631/frontend/jupiter/sql/managehost.html")
print("Press Enter to continue: ")
input("")
print("Scraping Started")
driver = login()
print("members started,wait it will take a while")
members(driver)
print(
    f"***************************members+members_progress completed {datetime.datetime.utcnow()}********************************")
print("alliance started,wait it will take a while")
alliance(driver)
print(
    f"***************************alliance+alliance_progress completed {datetime.datetime.utcnow()}********************************")
print("ranking started,wait it will take a while")
ranking(driver)
print(f"***************************ranking completed {datetime.datetime.utcnow()}********************************")
print("battles and new members started,wait it will take a while")
battles(driver)
print(f"***************************battles completed {datetime.datetime.utcnow()}********************************")
print("Scrap completed.")
print("thanks for using the program")
print("program exit")
