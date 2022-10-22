from flask import Flask, jsonify, request, redirect
import json
import requests

app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():
    dictToSend = {'rid': 2}
    res = requests.get('http://localhost:5000/view_info', json=dictToSend)
    print('test1')
    print(res.json())
    print('test2')
    return({'message': 'test'})

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5001, debug = True)