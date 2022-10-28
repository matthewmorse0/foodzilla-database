import mysql.connector
import getpass
import datetime


#Change password
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database='foodzilla',
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

    def get_restaurants(self):
        restaurants = self.Select("SELECT * from RESTAURANT;")
        return restaurants

    def get_info(self, rid: int):
        info = self.Select(f"SELECT * from restaurant WHERE rid = {rid};")
        return info

    def update_open_tables(self, rid: int, freeTables: str):
        self.Update(f"UPDATE RESTAURANT SET freeTables = '{freeTables}' WHERE rid = {rid};")

    def update_seating(self, rid: int, seating: str):
        self.Update(f"UPDATE RESTAURANT SET diningTables = '{seating}' WHERE rid = {rid};")

    def add_table(self, rid: int, xpos: int, ypos: int, seats: int):
        newid = self.Select(f"SELECT tbid from SEATING WHERE rid = {rid} ORDER BY tbid ASC;")
        nextid = 1
        for id in newid:
            if id[0] != nextid:
                break
            nextid = nextid + 1
        self.Update(f"INSERT INTO SEATING VALUES ({rid}, {xpos}, {ypos}, {nextid}, {seats}, True, '1:30:00');")
        return nextid

    def remove_table(self, rid: int, tbid: int):
        self.Update(f"DELETE FROM SEATING WHERE rid = {rid} AND tbid = {tbid};")

    def change_seat_num(self, rid: int, tbid: int, seatnum: int):
        self.Update(f"UPDATE SEATING SET seats = {seatnum} WHERE rid = {rid} AND tbid = {tbid};")

    def change_seating(self, rid: int, tblid: int):
        aval = self.Select(f"SELECT avaliable from SEATING WHERE rid = {rid} AND tbid = {tblid};")[0][0]
        self.Update(f"UPDATE SEATING SET avaliable = {not aval} WHERE rid = {rid} AND tbid = {tblid};")
        curtime = datetime.datetime.now().time()
        if aval:
            #seat is avaiable
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
        tables = self.Select(f"SELECT stime from SEATING WHERE rid = {rid} AND avaliable = {False} ORDER BY stime DESC;")
        numTables = self.Select(f"SELECT numTables from RINFO WHERE rid = {rid};")[0][0]
        if numTables > len(tables):
            return 0
        waitlist = self.Select(f"SELECT waitlist from RINFO WHERE rid = {rid};")[0][0]
        if waitlist >= numTables:
            return self.Select(f"SELECT ewait from RINFO WHERE rid = {rid};")[0][0] * 2
        nextTable = tables[waitlist]
        avgCust = self.Select(f"SELECT custTime, numCust from RINFO WHERE rid = {rid};")[0]
        avgCust = avgCust[0] / avgCust[1]
        curtime = datetime.datetime.now().time()
        return avgCust - (datetime.timedelta(hours= curtime.hour, minutes= curtime.minute, seconds= curtime.second) - nextTable[0]).total_seconds()

    def update_ewait(self, rid: int):
        self.Update(f"UPDATE RINFO SET ewait = {self.cal_ewait(rid)} WHERE rid = {rid};")

    def get_ewait(self, rid: int):
        return self.Select(f"SELECT ewait from RINFO WHERE rid = {rid};")[0]

    def change_waitlist(self, rid: int, num: int):
        self.Update(f"UPDATE RINFO SET waitlist = {num} WHERE rid = {rid};")
        return num
