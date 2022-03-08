#from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from planning_maker import PlanningMaker

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        next_week = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'
        print(next_week)
        """
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        #print(events_result)
        events = events_result.get('items', [])
        """
        print("Getting event for next week")
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              timeMax=next_week, singleEvents=True,
                                              orderBy='startTime').execute()
        # print(events_result)
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events

        night_start_hour = 22
        day_start_hour = 7

        #print(datetime.datetime.now().strftime(format="%V"))
        exclusion_times = []

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = event['start'].get('dateTime')
            end_time = event['end'].get('dateTime')
            # print(start_time, start, event['summary'])
            start_dt = datetime.datetime.fromisoformat(start_time)
            end_dt = datetime.datetime.fromisoformat(end_time)
            exclusion_times.append((start_dt, end_dt))
            #print(event_duration)
            #if start_dt.hour > night_start_hour or start_dt.hour < day_start_hour:
            #    print("night event")
            #else:
            #    print("day event")
            #print(start, event['summary'])

        #print([(x[0].strftime(format="%Y-%m-%dT%H:%M:%S"), x[1].strftime(format="%Y-%m-%dT%H:%M:%S")) for x in exclusion_times])
        user_timezone = start_dt.tzinfo
        test_planmaker = PlanningMaker(sleep_time=night_start_hour,
                                       wake_up_time=day_start_hour,
                                       user_timezone=user_timezone)
        test_planmaker.fill_in_scheduled_events(exclusion_times)
        test_schedule = test_planmaker.schedule_event(60)
        print(test_schedule)

        task = {"description": "this is a task"}
        print(task.description)
        # print(test_planmaker.busy_slots)

        # end = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z'
        # print(end)


        # calendar_list = service.calendarList().list().execute()

        # print(calendar_list)
        # for calendar in calendar_list.get('items', []):
        #    print(calendar["summary"])
        # event = service.events().insert(calendarId='primary', body=event).execute()
        # print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()