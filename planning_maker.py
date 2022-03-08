from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
import random

random.seed(123)
event_template = {
            'summary': 'Test',
            'description': 'Testing the Google Calendar API',
            'start': {
                'dateTime': "test_start",
            },
            'end': {
                'dateTime': "test_end",
            },
            }


class PlanningMaker:

    def __init__(self, sleep_time, wake_up_time, user_timezone):
        next_week_date = datetime.now() + relativedelta(weeks=1)
        target_week_number = next_week_date.strftime(format="%V")
        target_week_year = str(next_week_date.year)
        target_week_day = "1"
        str_week_format = ":".join([target_week_year, target_week_number, target_week_day])
        #print(str_week_format)
        # TODO: Get the user timedelta for timezone
        self.target_week_start = datetime.strptime(str_week_format, "%G:%V:%u").replace(tzinfo=user_timezone)
        print(self.target_week_start.tzinfo)
        #print(self.target_week_start)
        self.target_week_end = self.target_week_start + relativedelta(weeks=1)
        #print(self.target_week_end)
        self.sleep_time = sleep_time
        self.wake_up_time = wake_up_time
        self.scheduled_events = []

    def fill_in_scheduled_events(self, scheduled_events):
        self.scheduled_events = scheduled_events

    def check_planning_availability(self, event_start, event_end):
        """TODO: test all possible cases !"""
        event_ok = True
        for scheduled_event in self.scheduled_events:
            # print(scheduled_event[0].strftime(format="%Y-%m-%dT%H:%M:%S"),scheduled_event[1].strftime(format="%Y-%m-%dT%H:%M:%S"))
            # print(event_start.strftime(format="%Y-%m-%dT%H:%M:%S"), event_end.strftime(format="%Y-%m-%dT%H:%M:%S"))
            s_start = scheduled_event[0]
            s_end = scheduled_event[1]
            # First case : proposed event inside scheduled event:
            event_start_inside = (s_start <= event_start <= s_end)
            event_end_inside = (s_start <= event_end <= s_end)
            scheduled_is_inside = (s_start > event_start) & (s_end < event_end)
            # print(event_start_inside, event_end_inside, scheduled_is_inside)
            if event_start_inside or event_end_inside or scheduled_is_inside:
                event_ok = False
        # print(event_ok)
        return event_ok

    def schedule_event(self, duration, attempt=0, max_attempt=3):
        if max_attempt > 3:
            raise "Too many tries"
        event_day = random.choice(range(0, 8))
        event_hour = random.choice(range(self.wake_up_time, self.sleep_time-int(duration/60)-1))
        event_min = random.choice([0, 30])
        event_start = self.target_week_start + relativedelta(days=event_day, hours=event_hour, minutes=event_min)
        event_end = event_start + relativedelta(minutes=duration)
        # print(event_start, event_end)
        if not self.check_planning_availability(event_start, event_end):
            print("checking new timeslot")
            event_start, event_end = self.schedule_event(duration, attempt+1)
        return event_start, event_end

    def generate_events_from_tasks(self, task_list):
        event_list = []
        for task in task_list:
            event = event_template.copy()
            event["summary"] = task.summary
            event["description"] = task.description
            event_start, event_end = self.schedule_event(task.duration)
            event["start"]["datetime"] = event_start.isoformat() + 'Z'
            event["end"]["datetime"] = event_end.isoformat() + 'Z'
        return event_list


if __name__ == '__main__':
    import pytest
    pytest.main()
