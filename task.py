import uuid
import random
from datetime import datetime, timedelta


class Task:
    def __init__(self, summary, duration, description="", task_type="OTHER"):
        self.uid = uuid.uuid4()
        self.summary = summary
        self.description = description + f"\nTask_ID: {self.uid}"
        self.task_type = task_type
        self.duration = duration
        self.scheduled_time = None
        self.completed = False

    def get_scheduled_time(self):
        if self.scheduled_time is None:
            print("Task not scheduled")
            raise "Task not scheduled"
        else:
            return self.scheduled_time, self.scheduled_time + timedelta(
                minutes=self.duration
            )


class BucketList:
    def __init__(self):
        self.task_list = []

    def add_task(self, task):
        self.task_list.append(
            {"task_id": task.uid, "task": task, "created_date": datetime.now()}
        )

    def remove_task(self, task_id):
        for task_dict in self.task_list:
            if task_dict["task_id"] == task_id:
                self.task_list.remove(task_dict)


if __name__ == "__main__":
    import pytest

    pytest.main()
