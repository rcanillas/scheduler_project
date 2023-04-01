from kivy.app import App
from kivy.uix.widget import Widget
from random import random
from task import Task
from planning_maker import PlanningMaker

import google_calendar_handler as gch
import json

NIGHT_START_HOUR = 22
DAY_START_HOUR = 7


class SchedulingFrame(Widget):
    planning_maker = None
    def schedule_event(self, *args):
        event_name = self.ids["name_input"].text
        event_duration = self.ids["time_slider"].value
        print(f"Creating event {event_name} with duration {event_duration} min")
        task = Task(summary=event_name, duration=event_duration)
        print(task)
        event_list = self.planning_maker.generate_events_from_tasks([task])
        print(event_list)
        gch.add_events_to_calendar(event_list)


class SchedulingApp(App):
    future_events = gch.get_future_events()
    exclusion_times, user_timezone = gch.compute_exclusion_time(future_events)
    print(exclusion_times)
    planning_maker = PlanningMaker(
        sleep_time=NIGHT_START_HOUR,
        wake_up_time=DAY_START_HOUR,
        user_timezone=user_timezone,
    )
    planning_maker.fill_in_scheduled_events(exclusion_times)
    def build(self):
        app = SchedulingFrame()
        app.planning_maker = self.planning_maker
        return app


if __name__ == "__main__":
    SchedulingApp().run()
