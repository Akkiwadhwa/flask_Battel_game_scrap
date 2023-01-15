import time

import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def ranking():
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="db"
    )
    mycursor = mydb.cursor(buffered=True)

    try:
        b = "drop table members"
        mycursor.execute(b)
        mydb.commit()
    except:
        pass

    a = "CREATE TABLE IF NOT EXISTS members(Userid INT AUTO_INCREMENT PRIMARY KEY, Username varchar(255)" \
        "unique,ranking int(255),Total_Points int(255),Total_Bases float,alliance varchar(255))"
    mycursor.execute(a)
    mydb.commit()

    c = "INSERT INTO members(Username,ranking,Total_Points,Total_Bases,alliance) VALUES( %s, %s, %s,%s, %s)"

    url = "https://www.baseattackforce.com/"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    driver.find_element(By.ID, "loginname").send_keys("major81")
    driver.find_element(By.ID, "loginpass").send_keys("1122334455")
    driver.find_element(By.CLASS_NAME, "loginbut").click()
    time.sleep(3)
    for i in range(1, 977, 25):
        try:
            driver.get(f"https://www.baseattackforce.com/charts.php?s={i}")
            time.sleep(5)
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
                data = (
                    username, rank, points, bases, alliance
                )
                mycursor.execute(c, data)
                mydb.commit()
                print(mycursor.rowcount, "lines were inserted.")
        except Exception as e:
            print(e)
            pass

    driver.close()
    driver.quit()


while True:
    ranking()
    time.sleep(60 * 60 * 6)
