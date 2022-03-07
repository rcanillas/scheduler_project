import uuid


class Task:
    def __init__(self, name, user, duration, desc="", task_type="OTHER"):
        self.uid = uuid.uuid4()
        self.task_name = name
        self.user = user
        self.desc = desc
        self.task_type = task_type
        self.start_time = None
        self.duration = duration
        self.end_time = None
        self.scheduled = False

    def schedule_task(self, scheduled_time):
        self.start_time = scheduled_time
        self.end_time = self.start_time + self.duration
        self.scheduled = True


if __name__ == '__main__':
    import pytest
    pytest.main()
