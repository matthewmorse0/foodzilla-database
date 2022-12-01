from db import Database
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app)

db = Database()
@app.route("/get_all_info", methods=['GET'])
def get_all_restaurants():
    restaurants = db.get_restaurants()
    return jsonify({'restaurants': restaurants})

@app.route("/update_layout", methods=['POST'])
def update_seating_layout():
    rid = request.args.get('rid')
    seating = request.args.get('tables')
    oldtables = db.get_seating(rid)[0]
    oldtablesaval = db.get_tbids(rid)
    oldfree = db.get_freeseating(rid)
    freeTables = ''
    for x, i in enumerate(seating):
        if i != oldtables[x]:
            if x in oldtablesaval.keys() and oldtablesaval[x] != 0:
                db.remove_table(rid, x)
                freeTables += '0'
            elif int(i) == 1 or int(i) != int(oldtables[x]) + 1:
                db.add_table(rid, x, True)
                freeTables += '1'
            else:
                freeTables += oldfree[x]
        else:
            freeTables += oldfree[x]
    db.update_seating(rid, seating)
    db.update_open_tables(rid, freeTables)
    db.set_wait(rid, db.cal_ewait(rid))
    return {'message': 'updated seating'}

@app.route("/view_info", methods=['GET'])
def test():
    rid = request.args.get('rid')
    info = db.get_info(rid)
    return jsonify({'rest_info': info})

@app.route("/update_free", methods=['POST'])
def update_free_tables():
    rid = request.args.get('rid')
    freeTables = request.args.get('free')
    oldtables = db.get_tbids(rid)
    db.update_open_tables(rid, str(freeTables))
    x = 0
    for tb in freeTables:
        if x in oldtables.keys() and int(oldtables[x]) != int(tb):
            db.change_seating(rid, x)
        x = x + 1
    db.set_wait(rid, db.cal_ewait(rid))
    return {'message': 'updated free tables'}

@app.route("/add_waitlist", methods=['POST'])
def add_waitlist():
    rid = request.args.get('rid')
    db.add_waitlist(rid)
    db.set_wait(rid, db.cal_ewait(rid))
    return {'ewait': "done"}

@app.route("/remove_waitlist", methods=['POST'])
def remove_waitlist():
    rid = request.args.get('rid')
    db.remove_waitlist(rid)
    db.set_wait(rid, db.cal_ewait(rid))
    return {'ewait': "done"}
    
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)
