import datetime
import time
import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def members(driver):
    mydb = mysql.connector.connect(
        host="151.106.100.138",
        port=3306,
        user="nouahsar_admin",
        password="innovation1995",
        database="nouahsar_db"
    )
    mycursor = mydb.cursor()

    try:
        b = "drop table members"
        mycursor.execute(b)
        mydb.commit()
    except:
        pass

    a = "CREATE TABLE IF NOT EXISTS members(Userid INT AUTO_INCREMENT PRIMARY KEY, Username varchar(255)" \
        "unique,ranking int(255),Total_Points int(255),Total_Bases float,alliance varchar(255),Inserted_Date datetime,invitation int(255))"
    mycursor.execute(a)
    mydb.commit()

    a1 = "CREATE TABLE IF NOT EXISTS members_progress(Userid INT AUTO_INCREMENT PRIMARY KEY, Username varchar(255)" \
         ",ranking int(255),Total_Points int(255),Total_Bases float,alliance varchar(255),Inserted_Date datetime,invitation int(255))"
    mycursor.execute(a1)
    mydb.commit()

    c = "INSERT INTO members(Username,ranking,Total_Points,Total_Bases,alliance,Inserted_Date,invitation) VALUES( %s, %s, %s,%s, %s,%s,%s)"

    c1 = "INSERT INTO members_progress(Username,ranking,Total_Points,Total_Bases,alliance,Inserted_Date,invitation) VALUES( %s, %s, %s,%s, %s,%s,%s)"

    time.sleep(3)
    for i in range(1, 987, 25):
        try:
            mydb = mysql.connector.connect(
                host="151.106.100.138",
                port=3306,
                user="nouahsar_admin",
                password="innovation1995",
                database="nouahsar_db"
            )
            mycursor = mydb.cursor()
            driver.get(f"https://www.baseattackforce.com/charts.php?s={i}")
            time.sleep(3)
            data = driver.page_source
            soup = BeautifulSoup(data, "lxml")
            name = soup.find(class_="allyprofil")
            rows = name.find_all('tr')
            rows.pop(0)
            for i in rows:
                li = [i.text for i in i.find_all("td")]
                username = li[6]
                rank = li[0]
                points = li[2].replace("'", "")
                bases = li[4]
                alliance = li[8]
                date = datetime.datetime.now()
                value = None
                data = (
                    username, rank, points, bases, alliance, date,value
                )
                mycursor.execute(c, data)
                mydb.commit()
                mycursor.execute(c1, data)
                mydb.commit()
                print(f"{mycursor.rowcount} record(s) affected")
        except Exception as e:
            print(e)
            pass
