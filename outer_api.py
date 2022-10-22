from flask import Flask, jsonify, request, redirect
import json
import requests

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    dictToSend = {'rid': 2, 'free': '011|10'}
    res = requests.get('http://localhost:5000/view_info', json=dictToSend)
    print(res.json())
    res = requests.post('http://localhost:5000/update_free', json=dictToSend)
    dictToSend = {'rid': 2, 'tables': '822|35|45'}
    res = requests.post('http://localhost:5000/update_layout', json=dictToSend)
    res = requests.get('http://localhost:5000/view_info', json=dictToSend)
    print(res.json())
    return({'message': 'test'})

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5001, debug = True)