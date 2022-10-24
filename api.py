from db import Database
from flask import Flask, jsonify, request, redirect
import json
import requests

app = Flask(__name__)

db = Database()
@app.route("/get_all_info", methods=['GET'])
def get_all_restaurants():
    restaurants = db.get_restaurants()
    return jsonify({'restaurants': restaurants})

@app.route("/view_info", methods=['GET'])
def restaurant_storage():
    rid = request.get_json(force=True).get('rid')
    info = db.get_info(rid)
    return jsonify({'rest_info': info})

@app.route("/update_free", methods=['POST'])
def update_free_tables():
    rid = request.get_json(force=True).get('rid')
    freeTables = request.get_json(force=True).get('free')
    db.update_open_tables(rid, freeTables)
    return {'message': 'updated free tables'}

@app.route("/update_layout", methods=['POST'])
def update_seating_layout():
    rid = request.get_json(force=True).get('rid')
    seating = request.get_json(force=True).get('tables')
    freeTables = ''
    for i in seating:
        if i == '|':
            freeTables += '|'
        else:
            freeTables += '1'
    db.update_seating(rid, seating)
    db.update_open_tables(rid, freeTables)
    return {'message': 'updated seating'}
    

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)