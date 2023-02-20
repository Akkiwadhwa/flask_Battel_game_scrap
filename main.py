from alliance import alliance
from battles import battles
from members import members
from ranking import ranking
from alliance_protocal import alliance_protocal
from alliance_rundmails import alliance_rundmails
import datetime
from map_list import *

username = input("Username: ")
password = input("Password: ")
print("Scraping Started")
driver = login(username=username,password=password)
print("Maps started")
map_list(driver)
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
print("alliance_protocol started")
alliance_protocal(driver)
print(f"************************{datetime.datetime.utcnow()}***************************")
alliance_rundmails(driver)
print("Scrap completed.")
driver.close()
driver.quit()
print("thanks for using the program")
print("program exit")
