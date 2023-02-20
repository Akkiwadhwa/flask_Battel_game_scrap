import datetime
import time
import mysql.connector
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from login import login


def lost_units(driver):
    global username
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="db"
    )
    mycursor = mydb.cursor()


    a = "CREATE TABLE IF NOT EXISTS Lost_units(id INT AUTO_INCREMENT PRIMARY KEY,USERNAME TEXT,Date TEXT,MAP TEXT,Coordinates_X TEXT,Coordinates_Y TEXT,Attacker Text,Action Text,Units_type Text)"
    mycursor.execute(a)
    mydb.commit()
    c = "INSERT INTO Lost_units(USERNAME,DATE,MAP,Coordinates_X,Coordinates_Y,Attacker,Action,Units_type) VALUES( %s, %s, %s,%s, %s, %s,%s,%s) "
    url = "https://www.baseattackforce.com/gold?b=3"
    driver.get(url)
    time.sleep(3)
    a = driver.find_elements(By.TAG_NAME, "table")[1]
    b = a.find_elements(By.TAG_NAME, "tr")
    for i in b:
        li = [q.text.strip() for q in i.find_elements(By.TAG_NAME, "td")]
        li.pop(4)
        li.pop(5)
        username = str(username).capitalize()
        date = li[0]
        print(date)
        q = datetime.datetime.strptime(li[0], '%d.%m.%Y %H:%M').strftime('%Y.%m.%d %H:%M')
        print(q)
        map = li[1]
        x = li[2].split(":")[0]
        y = li[2].split(":")[1]
        attacker = li[3]
        action = li[4]
        unit = li[5]
        data = (username, date, map, x, y, attacker, action, unit)
        mycursor.execute(c, data)
        mydb.commit()
        print(f"{mycursor.rowcount} record(s) affected")


dict1 = {
    "AMJADNOUH": "a1s2d3",
    "MAJOR81": "1122334455",
    "KF22": "Rook700Jean956"
}

while True:
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="db"
    )
    mycursor = mydb.cursor()
    try:
        b = "drop table Lost_units"
        mycursor.execute(b)
        mydb.commit()
    except:
        pass

    for key, value in dict1.items():
        username = key
        password = value
        driver = login(username, password)
        lost_units(driver)
        driver.close()
        driver.quit()
    time.sleep(60 * 10)
