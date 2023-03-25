from flask import Flask, request, Response
from flask_crontab import Crontab

from task import Task
from planning_maker import PlanningMaker

import google_calendar_handler as gch
import json

print(__name__)
app = Flask(__name__)
app.debug = True
crontab = Crontab(app)

raw_task_list = []
transformed_task_list = []
DRY_RUN = True

NIGHT_START_HOUR = 22
DAY_START_HOUR = 7


def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    response.headers.add("Access-Control-Max-Age", "300")
    return response


@app.route("/", methods=["POST", "OPTIONS", "GET"])
def save_task():
    if request.method == "POST":
        print(request)
        print(request.data)
        task = json.loads(request.data)
        print(task["taskName"])
        response = Response(None, status=201, mimetype="application/json")
        response = add_cors_headers(response)
        raw_task_list.append(task)
        return response
    elif request.method == "OPTIONS":
        response = Response()
        response = add_cors_headers(response)
        print(response)
        print(response.headers)
        return response
    elif request.method == "GET":
        return "Hello World"


@crontab.job(minute="0", hour="17")
@app.route("/test_schedule", methods=["GET"])
def daily_task_scheduling():
    if DRY_RUN:
        if len(raw_task_list) == 0:
            raw_task_list.append({"taskName": "testTask", "taskDuration": 60})
    print("Scheduling started")
    # print(task_list)
    future_events = gch.get_future_events()
    exclusion_times, user_timezone = gch.compute_exclusion_time(future_events)
    print(exclusion_times)
    planning_maker = PlanningMaker(
        sleep_time=NIGHT_START_HOUR,
        wake_up_time=DAY_START_HOUR,
        user_timezone=user_timezone,
    )
    planning_maker.fill_in_scheduled_events(exclusion_times)

    for raw_task in raw_task_list:
        print(raw_task["taskName"])
        if "taskDescription" not in raw_task.keys():
            task = Task(summary=raw_task["taskName"], duration=raw_task["taskDuration"])
        else:
            task = Task(
                summary=raw_task["taskName"],
                duration=raw_task["taskDuration"],
                description=raw_task["taskDescription"],
            )
        transformed_task_list.append(task)
        raw_task_list.remove(raw_task)

    event_list = planning_maker.generate_events_from_tasks(transformed_task_list)
    print(event_list)
    if True:
        gch.add_events_to_calendar(event_list)
    print(raw_task_list)
    return "Testing scheduling"
