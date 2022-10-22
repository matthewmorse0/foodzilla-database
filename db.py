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

    def Select(self, sql: str):
        try:
            cursor = mydb.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except:
            print("Error: unable to fetch data")

    def Update(self, sql: str):
        try:
            cursor = mydb.cursor()
            cursor.execute(sql)
            mydb.commit()
        except:
            mydb.rollback()
            print("Error: unable to update")


    def get_info(self, rid: int):
        info = self.Select(f"SELECT * from restaurant WHERE rid = {rid};")
        return info

    def update_open_tables(self, rid: int, freeTables: str):
        self.Update(f"UPDATE RESTAURANT SET freeTables = '{freeTables}' WHERE rid = {rid};")

    def update_seating(self, rid: int, seating: str):
        self.Update(f"UPDATE RESTAURANT SET diningTables = '{seating}' WHERE rid = {rid};")