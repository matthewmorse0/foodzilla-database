from db import Database
from flask import Flask, jsonify, request, redirect
import json
import requests

app = Flask(__name__)

db = Database()
@app.route("/view_info", methods=['GET', 'POST'])
def restaurant_storage():
    rid = request.get_json(force=True).get('rid')
    info = db.get_info(rid)
    return jsonify({'rest_info': info})

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)