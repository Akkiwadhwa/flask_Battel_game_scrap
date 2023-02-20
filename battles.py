import time
import mysql.connector
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import datetime


def battles(driver):
    batt = []
    mydb = mysql.connector.connect(
        host="localhost",
        user="noua_admin",
        password="root",
        database="noua_db"
    )
    mycursor = mydb.cursor()
    try:
        b = "drop table battles"
        mycursor.execute(b)
        mydb.commit()
    except:
        pass

    a = "CREATE TABLE IF NOT EXISTS battles(id INT AUTO_INCREMENT PRIMARY KEY,date datetime,map varchar(255)," \
        "attacker varchar(255),action varchar(255),victim varchar(255)) "
    mycursor.execute(a)
    mydb.commit()

    c = "INSERT INTO battles(date,map,attacker,action,victim) VALUES( %s, %s, %s,%s,%s)"

    time.sleep(3)
    mydb = mysql.connector.connect(
        host="localhost",
        user="noua_admin",
        password="root",
        database="noua_db"
    )
    mycursor = mydb.cursor()
    d = "select Username from members"
    mycursor.execute(d)
    li3 = mycursor.fetchall()
    li_new = [w for i in li3 for w in i]
    for i in li_new:
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="noua_admin",
                password="root",
                database="noua_db")

            driver.get(f"https://www.baseattackforce.com/charts.php?a={i}&more=1")
            time.sleep(2)
            data = driver.page_source
            soup = BeautifulSoup(data, "lxml")
            mycursor = mydb.cursor()
            table = soup.find_all("table")[2]
            line = table.find_all("tr")
            for q in line:
                battle = ""
                li1 = [var.text for var in q.find_all("td")]
                date = li1[0] + " " + li1[1]
                map = li1[2].replace("MAP","")
                b = li1[3:]
                attacker = li1[3]
                action = li1[4]
                victim = li1[5]
                for p in b:
                    battle += p + " "
                if battle not in batt:
                    batt.append(battle)
                    data = (date, map,attacker,action,victim)
                    mycursor.execute(c, data)
                    mydb.commit()
                    print(f"{mycursor.rowcount} record(s) affected")
                if li1[3] not in li_new:
                    li_new.append(li1[3])
                    qu = "INSERT INTO members(Username,ranking,Total_Points,Total_Bases,alliance,Inserted_Date,invitation) VALUES( %s,%s, %s, %s,%s,%s)"
                    driver.get(f"https://www.baseattackforce.com/charts.php?a={li1[3]}")
                    time.sleep(2)
                    data = driver.page_source
                    try:
                        invite = driver.find_element(By.XPATH, "/html/body/center[2]/a[1]/button").text
                    except:
                        invite = None
                    if invite == "Invite this Player into your alliance":
                        i_value = 2
                    elif invite == "withdraw invitation":
                        i_value = 1
                    else:
                        i_value = 0
                    soup = BeautifulSoup(data, "lxml")
                    table = soup.find_all("table")[1]
                    line = table.find_all("td")
                    li = [i.text for i in line]
                    if 'Alliance:' in li:
                        alliance = li[li.index('Alliance:') + 1]
                    else:
                        alliance = None
                    name = li[li.index('Name:') + 1]
                    points = li[li.index('Points:') + 1].replace("'", "")
                    bases = li[li.index('Bases:') + 1]
                    rank = li[li.index('Charts Rank:') + 1].replace(">", "")
                    date = datetime.datetime.now()
                    data = (name, rank, points, bases, alliance, date, i_value)
                    mycursor.execute(qu, data)
                    mydb.commit()
                    print(f"{mycursor.rowcount} record(s) affected")
                if li1[5] not in li_new:
                    li_new.append(li1[5])
                    qu1 = "INSERT INTO members(Username,ranking,Total_Points,Total_Bases,alliance,Inserted_Date,invitation) VALUES( %s,%s, %s, %s,%s,%s)"
                    driver.get(f"https://www.baseattackforce.com/charts.php?a={li1[5]}")
                    time.sleep(2)
                    data = driver.page_source
                    try:
                        invite = driver.find_element(By.XPATH, "/html/body/center[2]/a[1]/button").text
                    except:
                        invite = None

                    if invite == "Invite this Player into your alliance":
                        i_value = 2
                    elif invite == "withdraw invitation":
                        i_value = 1
                    else:
                        i_value = 0
                    soup = BeautifulSoup(data, "lxml")
                    table = soup.find_all("table")[1]
                    line = table.find_all("td")
                    li = [i.text for i in line]
                    if 'Alliance:' in li:
                        alliance = li[li.index('Alliance:') + 1]
                    else:
                        alliance = None
                    name = li[li.index('Name:') + 1]
                    points = li[li.index('Points:') + 1].replace("'", "")
                    bases = li[li.index('Bases:') + 1]
                    date = datetime.datetime.now()
                    rank = li[li.index('Charts Rank:') + 1].replace(">", "")
                    data = (name, rank, points, bases, alliance, date, i_value)
                    mycursor.execute(qu1, data)
                    mydb.commit()
                    print(f"{mycursor.rowcount} record(s) affected")
        except Exception as e:
            print(e)
            pass
