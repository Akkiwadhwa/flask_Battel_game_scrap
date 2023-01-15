import datetime
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
        b = "drop table ranking"
        mycursor.execute(b)
        mydb.commit()
    except:
        pass

    a = "CREATE TABLE IF NOT EXISTS RANKING(id INT AUTO_INCREMENT PRIMARY KEY, Ranking int(255),Name varchar(255) " \
        "unique,Status varchar(255),Total_Points int(255),Total_Bases float,Total_Members TEXT,Democracy varchar(" \
        "255),Creation_Date TEXT,Language varchar(255),Requirements TEXT,Newcomers varchar(255),Date datetime) "
    mycursor.execute(a)
    mydb.commit()

    c = "INSERT INTO ranking(ranking,Name,Status,Total_Points,Total_Bases,Total_Members,Democracy,Creation_Date," \
        "Language,Requirements,Newcomers,Date) VALUES( %s, %s, %s, " \
        "%s, %s, %s, %s,%s, %s, %s, %s, %s)"

    url = "https://www.baseattackforce.com/"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    driver.find_element(By.ID, "loginname").send_keys("major81")
    driver.find_element(By.ID, "loginpass").send_keys("1122334455")
    driver.find_element(By.CLASS_NAME, "loginbut").click()
    time.sleep(3)
    driver.get("https://www.baseattackforce.com/ally.php?a=2")
    time.sleep(5)
    data = driver.page_source
    soup = BeautifulSoup(data, "lxml")
    name = soup.find_all(class_="allyprofil")
    rows = name[1].find_all('tr')
    rows.pop(0)
    for i in rows:
        try:
            li = [i.text for i in i.find_all("td")]
            rank = li[1]
            name = li[2].split(" ")[0]
            c_date = li[2].split(" ")[1]
            points = li[3].replace(".", "")
            bases = li[4]
            members = li[5]
            if "Requirements:" in li[6].split("Points")[0]:
                requirements = li[6].split("Points")[0] + "Points"
            else:
                requirements = None
            if int(points) + float(bases) + float(members) > 0:
                status = "EXIST"
            else:
                status = "EXTINCT"
            if "Democracy" in li[6]:
                democracy = "YES"
            else:
                democracy = "NO"
            language = li[6].split("language:")[1]
            if "Maps:" in language:
                language = language.split("Conquered")[0]
            else:
                pass
            if "newcomers are welcome" in li[6]:
                new_com = "newcomers are welcome"
            else:
                new_com = None
            date = datetime.datetime.now()
            data = (
                rank,
                name,
                status,
                points,
                bases,
                members,
                democracy,
                c_date,
                language,
                requirements,
                new_com,
                date
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
    time.sleep(60)
