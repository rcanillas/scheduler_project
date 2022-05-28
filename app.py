from flask import Flask, request, Response
import json
from flask_crontab import Crontab
from task import Task

print(__name__)
app = Flask(__name__)
app.debug = True
crontab = Crontab(app)

task_list = []
DRY_RUN = True

def add_CORS_headers(response):
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '300')
    return response


@app.route("/", methods=['POST', 'OPTIONS', 'GET'])
def save_task():
    if request.method == 'POST':
        print(request)
        print(request.data)
        task = json.loads(request.data)
        print(task["taskName"])
        response = Response(None, status=201, mimetype='application/json')
        response = add_CORS_headers(response)
        task_list.append(task)
        return response
    elif request.method == 'OPTIONS':
        response = Response()
        response = add_CORS_headers(response)
        print(response)
        print(response.headers)
        return response
    elif request.method == 'GET':
        return "Hello World"


@crontab.job(minute="0", hour="17")
@app.route("/test_schedule", methods=["GET"])
def daily_task_scheduling():
    if DRY_RUN:
        if len(task_list) == 0:
            task_list.append({"taskName": "testTask", "taskDuration": 60})
    print("Scheduling started")
    print(task_list)
    for task_to_schedule in task_list:
        print(task_to_schedule["taskName"])
        if "taskDescription" not in task_to_schedule.keys():
            task = Task(summary=task_to_schedule["taskName"],
                        duration=task_to_schedule["taskDuration"])
        else:
            task = Task(summary=task_to_schedule["taskName"],
                        duration=task_to_schedule["taskDuration"],
                        description=task_to_schedule["taskDescription"])
        print(task.summary)
        print(task.duration)
        print(task.description)
        task_list.remove(task_to_schedule)
    print(task_list)
    return "Testing scheduling"
