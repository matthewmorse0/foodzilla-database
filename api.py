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
    freeTables = ''
    for i in seating:
        if i == '|':
            freeTables += '|'
        elif i == '0':
            freeTables += '0'
        else:
            freeTables += '1'
    db.update_seating(rid, seating)
    db.update_open_tables(rid, freeTables)
    return {'message': 'updated seating'}

@app.route("/view_info", methods=['GET'])
def test():
    rid = request.args.get('rid')
    print('rid=', rid)
    info = db.get_info(rid)
    return jsonify({'rest_info': info})

@app.route("/update_free", methods=['POST'])
def update_free_tables():
    rid = request.args.get('rid')
    freeTables = request.args.get('free')
    print(f"rid={rid} free={freeTables}")
    db.update_open_tables(rid, str(freeTables))
    return {'message': 'updated free tables'}

@app.route("/add_table", methods=['POST'])
def add_table():
    rid = request.get_json(force=True).get('rid')
    xpos = request.get_json(force=True).get('xpos')
    ypos = request.get_json(force=True).get('ypos')
    seats = request.get_json(force=True).get('seats')
    newseat = db.add_table(rid, xpos, ypos, seats)
    return {'newseat': newseat}

@app.route("/remove_table", methods=['POST'])
def remove_table():
    rid = request.get_json(force=True).get('rid')
    tbid = request.get_json(force=True).get('tbid')
    newseat = db.remove_table(rid, tbid)
    return {'newseat': newseat}

@app.route("/change_seat_num", methods=['POST'])
def change_seat_num():
    rid = request.get_json(force=True).get('rid')
    tbid = request.get_json(force=True).get('tbid')
    seats = request.get_json(force=True).get('seats')
    newseat = db.change_seat_num(rid, tbid, seats)
    return {'newseat': newseat}

@app.route("/get_ewait", methods=['POST'])
def get_ewait():
    rid = request.get_json(force=True).get('rid')
    ewait = db.get_ewait(rid)
    return {'wait': ewait}

@app.route("/change_seating", methods=['POST'])
def change_seating():
    rid = request.get_json(force=True).get('rid')
    tbid = request.get_json(force=True).get('tbid')
    seat = db.change_seating(rid, tbid)
    return {'seat': seat}

@app.route("/update_ewait", methods=['POST'])
def update_ewait():
    rid = request.get_json(force=True).get('rid')
    ewait = db.update_ewait(rid)
    return {'ewait': ewait}
    

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)