import mysql.connector
from bs4 import BeautifulSoup



def alliance_protocal(driver):
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="nouahsar_admin",
        password="innovation1995",
        database="nouahsar_db"
    )
    mycursor = mydb.cursor(buffered=True)

    a = "CREATE TABLE IF NOT EXISTS alliance_protocal(id INT AUTO_INCREMENT PRIMARY KEY,Protocal TEXT,value int(255))"
    mycursor.execute(a)
    mydb.commit()

    b = "INSERT INTO alliance_protocal(Protocal,value) VALUES( %s, %s)"

    url = "https://www.baseattackforce.com/ally.php"
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, "lxml")
    name = soup.find_all(class_="allyprofil")
    rows = name[1].find_all('tr')
    try:
        for i in rows:
            if "Alliance protocol:" in i.text:
                want = i

        l1 = [q.text for q in want.find_all("font")]
        l1.pop(0)
        for i in l1:
            mydb = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="nouahsar_admin",
                password="innovation1995",
                database="nouahsar_db"
            )
            mycursor = mydb.cursor(buffered=True)
            pro = str(i.strip())
            if "invites" in pro:
                value = 2
            elif "withdraws invitation" in pro:
                value = 1
            elif "left the ally" in pro:
                value = 4
            elif "System takes" in pro:
                value = 3
            elif "kicked" in pro:
                value = 5
            else:
                value = 0

            data = (pro, value)
            mycursor.execute(b, data)
            mydb.commit()
            print(f"{mycursor.rowcount} record(s) affected")
    except Exception as e:
        print(e)
        pass


