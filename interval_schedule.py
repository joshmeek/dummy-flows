from prefect import task, Flow
from datetime import timedelta
from prefect.schedules import IntervalSchedule


@task
def say_hello():
    print("Hello, world!")


schedule = IntervalSchedule(interval=timedelta(minutes=2))

with Flow("interval-schedule", schedule) as flow:
    say_hello()

flow.register(project_name="QA")
