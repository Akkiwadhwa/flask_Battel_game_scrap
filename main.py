import datetime
import time
import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def alliance():
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="db"
    )
    mycursor = mydb.cursor(buffered=True)

    try:
        b = "drop table ALLIANCE"
        mycursor.execute(b)
        mydb.commit()
    except:
        pass

    a = "CREATE TABLE IF NOT EXISTS ALLIANCE(id INT AUTO_INCREMENT PRIMARY KEY,Name varchar(255) unique,Game_ID int(" \
        "255) " \
        "unique,Creation_Date TEXT,Status varchar(255),Approval int(1),Total_Points int(255),Total_Bases int(255)," \
        "Total_Members TEXT,Newcomers varchar(255),Requirements int(255),Democracy varchar(255),Language varchar(" \
        "255),Total_Maps int(255),Inserted_Date datetime) "
    mycursor.execute(a)
    mydb.commit()

    c = "INSERT INTO ALLIANCE(Name,Game_ID,Creation_Date,Status,Approval,Total_Points,Total_Bases,Total_Members," \
        "Newcomers,Requirements,Democracy,Language,Total_Maps,Inserted_Date) VALUES( %s, %s, %s, " \
        "%s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s)"

    url = "https://www.baseattackforce.com/"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    driver.find_element(By.ID, "loginname").send_keys("major81")
    driver.find_element(By.ID, "loginpass").send_keys("1122334455")
    driver.find_element(By.CLASS_NAME, "loginbut").click()
    time.sleep(3)
    for i in range(1, 999):
        try:
            print(i)
            driver.get(f"https://www.baseattackforce.com/ally.php?b={i}")
            time.sleep(3)
            data = driver.page_source
            soup = BeautifulSoup(data, "lxml")
            name = soup.find_all(class_="allyprofil")
            rows = name[1].find_all('td')
            li = [i.text for i in rows]
            print(li)
            alliance = li[li.index('Name of Alliance:') + 1]
            language = li[li.index('Alliance language:') + 1]
            if "minimum admission conditions: " in li:
                cond = li[li.index('minimum admission conditions: ') + 1]
            else:
                cond = None
            c_date = li[li.index('alliance creation date:') + 1]
            p = li[li.index('Points:') + 1]
            points = int(p.replace(".", "").strip())
            bases = li[li.index('Bases:') + 1]
            maps = li[li.index('Conquered Maps:') + 1]
            memb = li[li.index('Memb.:') + 1]
            newcomers = li[li.index('newcomers:') + 1]
            mem_new = li[li.index('Memb. + newcomers:') + 1]
            democracy = li[li.index('Democracy:') + 1]
            if points and bases and memb:
                status = "EXIST"
            else:
                status = "EXTINCT"
            approval = 0
            date = datetime.datetime.now()
            data = (
                alliance, i, c_date, status, approval, points, bases, memb, newcomers, cond, democracy, language, maps,
                date)
            mycursor.execute(c, data)
            mydb.commit()
            print(mycursor.rowcount, "lines were inserted.")
        except:
            pass

    driver.close()
    driver.quit()


while True:
    alliance()
    time.sleep(60 * 60 * 6)
