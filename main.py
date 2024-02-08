from scripts import kings_server, _922proxy, adprofex
from flask import Flask, jsonify


app = Flask(__name__)
@app.route('/api/selenium/<project_name>')
def selenium_route(project_name):

    if project_name == '922proxy':
        return jsonify(_922proxy.wallet())

    elif project_name == 'adprofex':
        return jsonify(adprofex.wallet())

    elif project_name == 'kings-server':
        return jsonify(kings_server.wallet())

    else:
        return 'Other project logic here'

if __name__ == '__main__':
    app.run(debug=True)
