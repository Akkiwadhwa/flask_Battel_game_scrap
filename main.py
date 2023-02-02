import requests
from alliance import alliance
from battles import battles
from members import members
from ranking import ranking
import datetime
print("Welcome to the scrapper.")
r = requests.get("https://api.ipify.org/").text
user = input("Enter BAF username: ")
password = input("Enter BAF password: ")
print(f"Your i.p is {r}")
print(
    "Please add this i.p  in your remote sql in cpanel --> https://www.nouahsark.com:2083/cpsess9648297631/frontend/jupiter/sql/managehost.html")
print("Press Enter to continue: ")
input("")
print("Scraping Started")
print("members started,wait it will take a while")
members(user, password)
print(f"***************************members+members_progress completed {datetime.datetime.utcnow()}********************************")
print("alliance started,wait it will take a while")
alliance(user, password)
print(f"***************************alliance+alliance_progress completed {datetime.datetime.utcnow()}********************************")
print("ranking started,wait it will take a while")
ranking(user, password)
print(f"***************************ranking completed {datetime.datetime.utcnow()}********************************")
print("battles and new members started,wait it will take a while")
battles(user, password)
print(f"***************************battles completed {datetime.datetime.utcnow()}********************************")
print("Scrap completed.")
print("thanks for using the program")
print("program exit")
