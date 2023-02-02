import datetime
import time
import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def alliance(user, password):
    mydb = mysql.connector.connect(
        host="151.106.100.138",
        port=3306,
        user="nouahsar_admin",
        password="innovation1995",
        database="nouahsar_db"
    )
    mycursor = mydb.cursor(buffered=True)

    try:
        b = "drop table alliance"
        mycursor.execute(b)
        mydb.commit()
    except:
        pass

    a = "CREATE TABLE IF NOT EXISTS alliance(id INT AUTO_INCREMENT PRIMARY KEY,Name varchar(255) unique,Game_ID int(" \
        "255) " \
        "unique,Creation_Date TEXT,Status varchar(255),Approval int(1),Total_Points int(255),Total_Bases int(255)," \
        "Total_Members int(255),Newcomers varchar(255),Requirements int(255),Democracy varchar(255),Language varchar(" \
        "255),Total_Maps int(255),Inserted_Date datetime) "
    mycursor.execute(a)
    mydb.commit()


    a1 = "CREATE TABLE IF NOT EXISTS alliance_progress(id INT AUTO_INCREMENT PRIMARY KEY,Name varchar(255),Game_ID int(" \
        "255) " \
        ",Creation_Date TEXT,Status varchar(255),Approval int(1),Total_Points int(255),Total_Bases int(255)," \
        "Total_Members int(255),Newcomers varchar(255),Requirements int(255),Democracy varchar(255),Language varchar(" \
        "255),Total_Maps int(255),Inserted_Date datetime) "
    mycursor.execute(a1)
    mydb.commit()

    c = "INSERT INTO alliance(Name,Game_ID,Creation_Date,Status,Approval,Total_Points,Total_Bases,Total_Members," \
        "Newcomers,Requirements,Democracy,Language,Total_Maps,Inserted_Date) VALUES( %s, %s, %s, " \
        "%s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s)"

    c1 = "INSERT INTO alliance_progress(Name,Game_ID,Creation_Date,Status,Approval,Total_Points,Total_Bases,Total_Members," \
        "Newcomers,Requirements,Democracy,Language,Total_Maps,Inserted_Date) VALUES( %s, %s, %s, " \
        "%s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s)"

    url = "https://www.baseattackforce.com/"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    driver.find_element(By.ID, "loginname").send_keys(user)
    driver.find_element(By.ID, "loginpass").send_keys(password)
    driver.find_element(By.CLASS_NAME, "loginbut").click()
    time.sleep(3)
    mydb = mysql.connector.connect(
        host="151.106.100.138",
        port=3306,
        user="nouahsar_admin",
        password="innovation1995",
        database="nouahsar_db"
    )
    mycursor = mydb.cursor()
    for i in range(10, 500):
        try:
            driver.get(f"https://www.baseattackforce.com/ally.php?b={i}")
            time.sleep(3)
            data = driver.page_source
            soup = BeautifulSoup(data, "lxml")
            name = soup.find_all(class_="allyprofil")
            rows = name[1].find_all('td')
            li = [i.text for i in rows]
            alliance = li[li.index('Name of Alliance:') + 1]
            language = li[li.index('Alliance language:') + 1]
            if "minimum admission conditions: " in li:
                cond = li[li.index('minimum admission conditions: ') + 1]
            else:
                cond = None
            c_date = datetime.datetime.strptime(li[li.index('alliance creation date:') + 1], '%d.%m.%Y').strftime('%Y.%m.%d')
            p = li[li.index('Points:') + 1]
            points = int(float(p.replace(".", "").strip()))
            bases = int(float(li[li.index('Bases:') + 1]))
            maps = li[li.index('Conquered Maps:') + 1].replace("/ 50","")
            memb = li[li.index('Memb.:') + 1]
            newcomers = li[li.index('newcomers:') + 1]
            democracy = li[li.index('Democracy:') + 1]
            if points + bases > 0:
                status = "EXIST"
            else:
                status = "EXTINCT"
            approval = 1
            date = datetime.datetime.now()
            data = (
                alliance, i, c_date, status, approval, points, bases, memb, newcomers, cond, democracy, language, maps,
                date)
            mycursor.execute(c, data)
            mydb.commit()
            mycursor.execute(c1, data)
            mydb.commit()
        except Exception as e:
            print(e)
            pass

    driver.close()
    driver.quit()
