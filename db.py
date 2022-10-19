import mysql.connector

#Change password
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database='foodzilla',
    password="Pass1234"
)

def Select(sql):
    try:
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except:
        print("Error: unable to fetch data")

def main():
    rid = 1
    test = Select(f"SELECT * from restaurant where rid = {rid};")
    print(test)


main()