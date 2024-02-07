from scripts import kings_server, _922proxy, adprofex
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/api/selenium/922proxy')
def route_922proxy_():
    wallet = _922proxy._922proxy()
    return jsonify(wallet)

@app.route('/api/selenium/adprofex')
def route_adprofex():
    wallet = adprofex.adprofex()
    return jsonify(wallet)

@app.route('/api/selenium/king_server')
def route_king_server():
    wallet = kings_server.king_server_wallet()
    return jsonify(wallet)

if __name__ == "__main__":
    app.run(debug=True)