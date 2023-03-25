import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
]

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

except HttpError as error:
    print("An error occurred: %s" % error)


def get_past_events(research_time=datetime.datetime.utcnow()):
    now = research_time.isoformat() + "Z"
    last_week = (research_time - datetime.timedelta(days=7)).isoformat() + "Z"
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
    past_events = past_events_result.get("items", [])
    return past_events


def get_future_events(research_time=datetime.datetime.utcnow()):
    now = research_time.isoformat() + "Z"
    next_week = (research_time + datetime.timedelta(days=7)).isoformat() + "Z"
    future_events_result = (
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
    future_events = future_events_result.get("items", [])
    return future_events


def insert_events(event_list):
    for event in event_list:
        pass
        event = json.dumps(event)
        print(event)
        event = service.events().insert(calendarId="primary", body=event).execute()
        print("Event created: %s" % (event.get("htmlLink")))


def compute_exclusion_time(future_events):
    exclusion_times = []
    for event in future_events:
        # print(event)
        if "dateTime" in event["start"].keys():
            start_time = event["start"].get("dateTime")
            end_time = event["end"].get("dateTime")
            start_dt = datetime.datetime.fromisoformat(start_time)
            end_dt = datetime.datetime.fromisoformat(end_time)
            user_tzinfo = start_dt.tzinfo
        elif "date" in event["start"].keys():
            print(event["start"].keys())
            start_time = event["start"].get("date")
            end_time = event["end"].get("date")
            start_dt = datetime.datetime.fromisoformat(start_time)
            start_dt = start_dt.replace(tzinfo=user_tzinfo)
            end_dt = datetime.datetime.fromisoformat(end_time)
            end_dt = end_dt.replace(tzinfo=user_tzinfo)
        exclusion_times.append((start_dt, end_dt))

    return exclusion_times, user_tzinfo


def add_events_to_calendar(event_list):
    for event in event_list:
        event = service.events().insert(calendarId="primary", body=event).execute()
        print("Event created: %s" % (event.get("htmlLink")))
