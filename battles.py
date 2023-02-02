import time
import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def battles(user, password):
    batt = []
    mydb = mysql.connector.connect(
        host="151.106.100.138",
        port=3306,
        user="nouahsar_admin",
        password="innovation1995",
        database="nouahsar_db"
    )
    mycursor = mydb.cursor(buffered=True)

    try:
        b = "drop table battles"
        mycursor.execute(b)
        mydb.commit()
    except:
        pass

    a = "CREATE TABLE IF NOT EXISTS battles(id INT AUTO_INCREMENT PRIMARY KEY,date datetime,map varchar(255)," \
        "battle varchar(255)) "
    mycursor.execute(a)
    mydb.commit()

    c = "INSERT INTO battles(date,map,battle) VALUES( %s, %s, %s)"

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
    d = "select Username from members"
    mycursor.execute(d)
    li3 = mycursor.fetchall()
    li_new = [w for i in li3 for w in i]
    for i in li_new:
        try:
            driver.get(f"https://www.baseattackforce.com/charts.php?a={i}&more=1")
            time.sleep(2)
            data = driver.page_source
            soup = BeautifulSoup(data, "lxml")
            table = soup.find_all("table")[2]
            line = table.find_all("tr")
            for q in line:
                battle = ""
                li1 = [var.text for var in q.find_all("td")]
                date = li1[0] + " " + li1[1]
                map = li1[2]
                b = li1[3:]
                for p in b:
                    battle += p + " "
                if battle not in batt:
                    batt.append(battle)
                    data = (date, map, battle)
                    mycursor.execute(c, data)
                    mydb.commit()
                if li1[3] not in li_new:
                    li_new.append(li1[3])
                    qu = "INSERT INTO members(Username,ranking,Total_Points,Total_Bases,alliance) VALUES( %s, %s, %s,%s,%s)"
                    driver.get(f"https://www.baseattackforce.com/charts.php?a={li1[3]}")
                    time.sleep(2)
                    data = driver.page_source
                    soup = BeautifulSoup(data, "lxml")
                    table = soup.find_all("table")[1]
                    line = table.find_all("td")
                    li = [i.text for i in line]
                    if 'Alliance:' in li:
                        alliance = li[li.index('Alliance:') + 1]
                    else:
                        alliance = None
                    name = li[li.index('Name:') + 1]
                    points = li[li.index('Points:') + 1]
                    bases = li[li.index('Bases:') + 1]
                    rank = li[li.index('Charts Rank:') + 1]
                    data = (name, rank, points, bases, alliance)
                    mycursor.execute(qu, data)
                    mydb.commit()
                if li1[5] not in li_new:
                    li_new.append(li1[5])
                    qu1 = "INSERT INTO members(Username,ranking,Total_Points,Total_Bases,alliance) VALUES( %s, %s, %s,%s,%s)"
                    driver.get(f"https://www.baseattackforce.com/charts.php?a={li1[5]}")
                    time.sleep(2)
                    data = driver.page_source
                    soup = BeautifulSoup(data, "lxml")
                    table = soup.find_all("table")[1]
                    line = table.find_all("td")
                    li = [i.text for i in line]
                    if 'Alliance:' in li:
                        alliance = li[li.index('Alliance:') + 1]
                    else:
                        alliance = None
                    name = li[li.index('Name:') + 1]
                    points = li[li.index('Points:') + 1]
                    bases = li[li.index('Bases:') + 1]
                    rank = li[li.index('Charts Rank:') + 1]
                    data = (name, rank, points, bases, alliance)
                    mycursor.execute(qu1, data)
                    mydb.commit()
        except Exception as e:
            print(e)
            pass

    driver.close()
    driver.quit()
