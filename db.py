import mysql.connector
import getpass
import datetime

sqlPass = getpass.getpass("Password")

#Change password
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database='foodzilla',
    password=sqlPass
)

class Database:
    def __init__(self):
        seating = []
        freeseating = []
        curtime = datetime.datetime.now().time()
        for i in range(1, 5):
            seating.append(self.Select(f"SELECT diningTables from RESTAURANT WHERE rid = {i};"))
            freeseating.append(self.Select(f"SELECT freeTables from RESTAURANT WHERE rid = {i};"))
        for x, res in enumerate(seating):
            for y, seat in enumerate(res[0][0]):
                if seat != '0' and seat != '|':
                    self.Update(f"REPLACE INTO SEATING VALUES ({x+1}, {y} , {bool(int(freeseating[x][0][0][y]))}, '{str(datetime.timedelta(hours=curtime.hour, minutes=curtime.minute, seconds=curtime.second))}');")
                    self.Update(f"UPDATE RESTAURANT SET waitlist = 0, waittime = 30;")
                    self.Update(f"UPDATE RINFO SET numCust = 1, custTime = 1800;")
        for i in range(1, 5):
            self.set_wait(i, self.cal_ewait(i))

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
        except Exception as e:
            mydb.rollback()
            print("Error: unable to update")
            print(e)

    def get_restaurants(self):
        for i in range(1, 5):
            self.set_wait(i, self.cal_ewait(i))
        restaurants = self.Select("SELECT * from RESTAURANT;")
        return restaurants

    def get_info(self, rid: int):
        info = self.Select(f"SELECT * from restaurant WHERE rid = {rid};")
        return info

    def update_open_tables(self, rid: int, freeTables: str):
        self.Update(f"UPDATE RESTAURANT SET freeTables = '{freeTables}' WHERE rid = {rid};")

    def update_seating(self, rid: int, seating: str):
        self.Update(f"UPDATE RESTAURANT SET diningTables = '{seating}' WHERE rid = {rid};")

    def update_open_tables(self, rid: int, freeTables: str):
        self.Update(f"UPDATE RESTAURANT SET freeTables = '{freeTables}' WHERE rid = {rid};")

    def update_seating(self, rid: int, seating: str):
        self.Update(f"UPDATE RESTAURANT SET diningTables = '{seating}' WHERE rid = {rid};")

    def get_seating(self, rid: int):
        return self.Select(f"SELECT diningTables from RESTAURANT WHERE rid = {rid};")[0]

    def get_freeseating(self, rid: int):
        return self.Select(f"SELECT freeTables from RESTAURANT WHERE rid = {rid};")[0][0]
    
    def get_tbids(self, rid: int):
        return {tb[0]: tb[1] for tb in self.Select(f"SELECT tbid, avaliable from SEATING WHERE rid = {rid};")}

    def set_wait(self, rid: int, ewait: int):
        self.Update(f"UPDATE RESTAURANT SET waitTime = {ewait} WHERE rid = {rid};")

    def add_table(self, rid: int, tbid: int, aval: bool):
        curtime = datetime.datetime.now().time()
        self.Update(f"INSERT INTO SEATING VALUES ({rid}, {tbid} , {aval}, '{str(datetime.timedelta(hours=curtime.hour, minutes=curtime.minute, seconds=curtime.second))}');")
        self.Update(f"UPDATE RINFO SET numTables = numTables + 1 WHERE rid = {rid};")

    def remove_table(self, rid: int, tbid: int):
        self.Update(f"DELETE FROM SEATING WHERE rid = {rid} AND tbid = {tbid};")
        self.Update(f"UPDATE RINFO SET numTables = numTables - 1 WHERE rid = {rid};")

    def change_seating(self, rid: int, tblid: int):
        aval = self.Select(f"SELECT avaliable from SEATING WHERE rid = {rid} AND tbid = {tblid};")[0][0]
        self.Update(f"UPDATE SEATING SET avaliable = {not aval} WHERE rid = {rid} AND tbid = {tblid};")
        curtime = datetime.datetime.now().time()
        if aval:
            #seat is now seated
            self.Update(f"UPDATE SEATING SET stime = '{str(datetime.timedelta(hours=curtime.hour, minutes=curtime.minute, seconds=curtime.second))}' WHERE rid = {rid} AND tbid = {tblid};")
        else:
            self.Update(f"UPDATE RINFO SET custTime = custTime + {self.get_seated_time(rid, tblid).total_seconds()} WHERE rid = {rid};")
            self.Update(f"UPDATE RINFO SET numCust = numCust + {1} WHERE rid = {rid};")
        return not aval
            
    def get_seated_time(self, rid: int, tblid: int):
        t = self.Select(f"SELECT stime from SEATING WHERE rid = {rid} AND tbid = {tblid};")[0][0]
        curtime = datetime.datetime.now().time()
        return (datetime.timedelta(hours=curtime.hour, minutes=curtime.minute, seconds=curtime.second) - t)

    def cal_ewait(self, rid: int):
        tables = self.Select(f"SELECT stime from SEATING WHERE rid = {rid} AND avaliable = False  ORDER BY stime ASC;")
        numTables = self.Select(f"SELECT numTables from RINFO WHERE rid = {rid};")[0][0]
        waitlist = self.Select(f"SELECT waitlist from RESTAURANT WHERE rid = {rid};")[0][0]
        if numTables > (waitlist + len(tables)):
            return 0
        if waitlist >= numTables:
            return self.Select(f"SELECT waitTime from RESTAURANT WHERE rid = {rid};")[0][0] * 2
        nextTable = tables[waitlist]
        avgCust = self.Select(f"SELECT custTime, numCust from RINFO WHERE rid = {rid};")[0]
        avgCust = avgCust[0] / avgCust[1]
        curtime = datetime.datetime.now().time()
        return (avgCust - (datetime.timedelta(hours= curtime.hour, minutes= curtime.minute, seconds= curtime.second) - nextTable[0]).total_seconds()) / 60

    def add_waitlist(self, rid: int):
        self.Update(f"UPDATE RESTAURANT SET waitlist = waitlist + 1 WHERE rid = {rid};")

    def remove_waitlist(self, rid: int):
        if self.Select(f"SELECT waitlist from RESTAURANT where rid = {rid};")[0][0] != 0:
            self.Update(f"UPDATE RESTAURANT SET waitlist = waitlist - 1 WHERE rid = {rid};")
