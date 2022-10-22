import mysql.connector

#Change password
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database='foodzilla',
    password="Pass1234"
)

class Database:
    def __init__(self):
        pass

    def Select(self, sql):
        try:
            cursor = mydb.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except:
            print("Error: unable to fetch data")

    def get_info(self, rid: int):
        info = self.Select(f"SELECT * from restaurant where rid = {rid};")
        return info
