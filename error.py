from typing import List, Dict
import logging
import prefect
from prefect import Flow
from prefect import Task
from prefect.triggers import any_failed
from prefect import unmapped

# prefect_logger = prefect.utilities.logging.get_logger()
# prefect_logger.setLevel(logging.INFO)


class TaskA(Task):
    def run(self) -> List[Dict]:
        print("Starting A")
        records = [
            {"data": "dummy"},
            {"data": "dummier"},
            {"data": "dummiest"},
        ]
        return records


class TaskB(Task):
    def run(self) -> None:
        print("Starting B")
        print("doing something unrelated")


class TaskC(Task):
    def run(self, data: List) -> None:
        print("Starting C")
        # raise RuntimeError("Uncomment this to fix")
        print(f"Data: {data}")


class TaskD(Task):
    def run(self, data: List) -> None:
        print("Starting D")
        print("Cleaning up failure")


task_a = TaskA()
task_b = TaskB()
task_c = TaskC()
task_d = TaskD(trigger=any_failed)


with Flow("dummy_flow") as flow:
    task_c_ref = task_c.map(data=task_a, upstream_tasks=[unmapped(task_b)])
    task_d.map(data=task_a, upstream_tasks=[unmapped(task_c_ref)])

# flow.visualize()
flow.run()