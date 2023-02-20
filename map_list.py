import time

import mysql.connector
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from login import login


def map_list(driver):
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="db"
    )
    mycursor = mydb.cursor()


    a = "CREATE TABLE IF NOT EXISTS maps(id INT AUTO_INCREMENT PRIMARY KEY, Maps int(255))"
    mycursor.execute(a)
    mydb.commit()

    c = "INSERT INTO maps(Maps) VALUES( %s)"

    drawing = ActionChains(driver).move_by_offset(1001, 350).click()
    drawing.perform()
    print(driver.get_window_size())
    time.sleep(2)
    a = driver.find_elements(By.CLASS_NAME, "mwbut2")
    b = driver.find_elements(By.CLASS_NAME, "mwbut1")
    for i in a:
        try:
            map_num = i.text.strip()
            print(map_num)
            mycursor.execute(c, (map_num,))
            mydb.commit()
            print(f"{mycursor.rowcount} record(s) affected")
        except:
            pass

    for i in b:
        try:
            map_num = i.text.strip()
            print(map_num)
            mycursor.execute(c, (map_num,))
            mydb.commit()
            print(f"{mycursor.rowcount} record(s) affected")
        except:
            pass


driver = login("major81", "1122334455")
map_list(driver)
