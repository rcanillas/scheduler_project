# from __future__ import print_function

import datetime
import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from planning_maker import PlanningMaker
from preference_analyzer import PreferenceAnalyzer
from task import Task

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        next_week = (
            datetime.datetime.utcnow() + datetime.timedelta(days=7)
        ).isoformat() + "Z"
        last_week = (
            datetime.datetime.utcnow() - datetime.timedelta(days=7)
        ).isoformat() + "Z"
        print(next_week)
        """
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        #print(events_result)
        events = events_result.get('items', [])
        """

        print("Getting event for last week")
        old_task = Task(
            summary="Old Test task",
            duration=60,
            description="This is a test task for completion",
        )
        old_task.uid = "2489038b-34d0-4afb-b4ff-6ab4623bca33"
        old_event = {
            "summary": old_task.summary,
            "description": old_task.description,
            "start": {},
            "end": {},
        }
        print(old_event)
        # print(event_start, event_end)
        # print(event_start.isoformat(), event_end.isoformat())
        # print("old task id:", old_task.uid)
        past_events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=last_week,
                timeMax=now,
                singleEvents=True,
                orderBy="startTime",
                showDeleted=True,
            )
            .execute()
        )
        # print(events_result)
        old_task_found = False
        past_events = past_events_result.get("items", [])
        for past_event in past_events:
            print(past_event["summary"])
            if "description" in past_event.keys():
                print(past_event["description"])
                if str(old_task.uid) in past_event["description"]:
                    old_task_found = True
                    old_task_start = past_event["start"].get("dateTime")
                    old_task_start_dt = datetime.datetime.fromisoformat(old_task_start)
                    old_task_start_padded = old_task_start_dt - datetime.timedelta(
                        minutes=old_task_start_dt.minute
                    )
                    old_task.scheduled_time = old_task_start_padded
                    if past_event["status"] == "confirmed":
                        old_task.completed = True
                    else:
                        old_task.completed = False
            print(past_event["status"])
            print()

        print("old task found:", old_task_found)
        if not old_task_found:
            old_event["start"]["dateTime"] = (
                datetime.datetime.utcnow() - datetime.timedelta(days=6)
            ).isoformat() + "Z"
            old_event["end"]["dateTime"] = (
                datetime.datetime.utcnow()
                - datetime.timedelta(days=6)
                + datetime.timedelta(minutes=old_task.duration)
            ).isoformat() + "Z"
            old_event = (
                service.events().insert(calendarId="primary", body=old_event).execute()
            )
            print("Old event created: %s" % (old_event.get("htmlLink")))

        print("Getting event for next week")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                timeMax=next_week,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        # print(events_result)
        events = events_result.get("items", [])
        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events

        night_start_hour = 22
        day_start_hour = 7

        # print(datetime.datetime.now().strftime(format="%V"))
        exclusion_times = []

        for event in events:
            # start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = event["start"].get("dateTime")
            end_time = event["end"].get("dateTime")
            # print(start_time, start, event['summary'])
            # print(event)
            # if "description" in event.keys():
            #    print(event["description"])
            # print()
            start_dt = datetime.datetime.fromisoformat(start_time)
            end_dt = datetime.datetime.fromisoformat(end_time)
            exclusion_times.append((start_dt, end_dt))
            # print(event_duration)
            # if start_dt.hour > night_start_hour or start_dt.hour < day_start_hour:
            #    print("night event")
            # else:
            #    print("day event")
            # print(start, event['summary'])

        # print([(x[0].strftime(format="%Y-%m-%dT%H:%M:%S"), x[1].strftime(format="%Y-%m-%dT%H:%M:%S")) for x in exclusion_times])
        user_timezone = start_dt.tzinfo
        test_planmaker = PlanningMaker(
            sleep_time=night_start_hour,
            wake_up_time=day_start_hour,
            user_timezone=user_timezone,
        )
        test_planmaker.fill_in_scheduled_events(exclusion_times)
        # test_schedule = test_planmaker.schedule_event(60)
        # print(test_schedule)

        task = Task(summary="Test task", duration=60, description="This is a test task")
        task2 = Task(
            summary="Test task 2", duration=30, description="This is a second test task"
        )
        task3 = Task(
            summary="Small swarm task",
            duration=10,
            description="Swarm tasks are lot of small tasks",
        )
        task2.completed = True
        task_list = [task, task2]
        # task_list = [task3] * 5
        event_list = test_planmaker.generate_events_from_tasks(task_list)
        for event in event_list:
            event = json.dumps(event)
            print(event)
            event = service.events().insert(calendarId="primary", body=event).execute()
            print("Event created: %s" % (event.get("htmlLink")))

        # print(task.description)
        # print(test_planmaker.busy_slots)

        # end = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z'
        # print(end)

        # calendar_list = service.calendarList().list().execute()

        # print(calendar_list)
        # for calendar in calendar_list.get('items', []):
        #    print(calendar["summary"])
        # event = service.events().insert(calendarId='primary', body=event).execute()
        # print('Event created: %s' % (event.get('htmlLink')))
        old_task_list = [old_task]
        plan_analyzer = PreferenceAnalyzer()
        plan_analyzer.update_timeslots(old_task_list)
        pref_dict = plan_analyzer.preference_dict
        for key, value in pref_dict.items():
            if value != 0 and value is not None:
                print(key, value)

    except HttpError as error:
        print("An error occurred: %s" % error)


if __name__ == "__main__":
    main()
