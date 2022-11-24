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
    

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)