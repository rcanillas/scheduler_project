from task import Task
from datetime import timedelta, datetime


class TestTask:
    def test_init(self):
        test_duration = timedelta(seconds=10)
        test_task = Task(
            name="test", user="test", duration=test_duration, desc="", task_type="OTHER"
        )
        assert test_task.task_name == "test"
        assert test_task.user == "test"
        assert test_task.duration == test_duration
        assert test_task.desc == ""
        assert test_task.task_type == "OTHER"

    def test_schedule(self):
        test_duration = timedelta(seconds=10)
        test_schedule_time = datetime.now()
        test_task = Task(
            name="test", user="test", duration=test_duration, desc="", task_type="OTHER"
        )
        test_task.schedule_task(test_schedule_time)
        assert test_task.end_time == test_schedule_time + test_duration
        assert test_task.scheduled
