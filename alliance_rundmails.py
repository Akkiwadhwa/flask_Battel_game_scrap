import mysql.connector
from bs4 import BeautifulSoup



def alliance_rundmails(driver):
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="nouahsar_admin",
        password="innovation1995",
        database="nouahsar_db"
    )
    mycursor = mydb.cursor(buffered=True)

    a = "CREATE TABLE IF NOT EXISTS alliance_rundmails(id INT AUTO_INCREMENT PRIMARY KEY,Date TEXT,Sender TEXT,Message TEXT)"
    mycursor.execute(a)
    mydb.commit()

    b = "INSERT INTO alliance_rundmails(Date,Sender,Message) VALUES( %s, %s,%s)"
    global want

    url = "https://www.baseattackforce.com/ally.php"
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, "lxml")
    name = soup.find_all(class_="allyprofil")
    rows = name[1].find_all('tr')
    try:
        for i in rows:
            if "Ally-Rundmails:" in i.text:
                want = i

        l1 = [q.text for q in want.find_all("b")]
        l2 = [q.text for q in want.find_all("i")]

        for i in range(0, len(l1)):
            mydb = mysql.connector.connect(
                host="151.106.100.138",
                port=3306,
                user="nouahsar_admin",
                password="innovation1995",
                database="nouahsar_db"
            )
            mycursor = mydb.cursor(buffered=True)

            date = str(l1[i]).split()[0] + " " + str(l1[i]).split()[1]
            sender = str(l1[i]).split()[2].replace(":", "")
            message = l2[i]
            data = (date, sender, message)
            mycursor.execute(b, data)
            mydb.commit()
            print(f"{mycursor.rowcount} record(s) affected")
    except Exception as e:
        print(e)
        pass

