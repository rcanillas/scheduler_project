from datetime import datetime, time
from dateutil.relativedelta import relativedelta


class PreferenceAnalyzer:

    def __init__(self, task_type="All", night_start=time(hour=22, minute=0, second=0),
                 day_start=time(hour=7, minute=0, second=0), timeslot_duration=30):
        timeslot = datetime.strptime("2012:01:1", "%G:%V:%u")
        timeslot_end = timeslot + relativedelta(weeks=1)
        self.preference_dict = {}
        self.task_type = task_type
        self.timeslot_duration = timeslot_duration
        while timeslot < timeslot_end:
            if night_start > timeslot.time() > day_start:
                self.preference_dict[timeslot.strftime(format="%u-%H:%M")] = 0
            else:
                self.preference_dict[timeslot.strftime(format="%u-%H:%M")] = None
            timeslot += relativedelta(minutes=timeslot_duration)
        #print(len(self.preference_dict))
        #print(self.preference_dict)

    def update_timeslots(self, task_list):
        for task in task_list:
            if task.scheduled_time is not None:
                task_start, task_end = task.get_scheduled_time()
                timeslot = task_start
                while timeslot < task_end:
                    timeslot_key = timeslot.strftime(format="%u-%H:%M")
                    if task.completed:
                        self.preference_dict[timeslot_key] += 1
                    else:
                        self.preference_dict[timeslot_key] -= 1
                    timeslot += relativedelta(minutes=self.timeslot_duration)
                    print(task_start, task_end)
                    print(self.preference_dict[timeslot_key])


if __name__ == '__main__':
    import pytest
    pytest.main()

