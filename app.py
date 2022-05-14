from flask import Flask, request, Response
import json

print(__name__)
app = Flask(__name__)
app.debug = True


def add_CORS_headers (response):
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '300')
    return response


@app.route("/", methods=['POST', 'OPTIONS', 'GET'])
def save_json():
    if request.method == 'POST':
        print(request)
        print(request.data)
        task = json.loads(request.data)
        print(task["taskName"])
        response = Response(None, status=201, mimetype='application/json')
        response = add_CORS_headers(response)
        return response
    elif request.method == 'OPTIONS':
        response = Response()
        response = add_CORS_headers(response)
        print(response)
        print(response.headers)
        return response
    elif request.method == 'GET':
        return "Hello World"
