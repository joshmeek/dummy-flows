from prefect import task, Flow
from datetime import timedelta, datetime
from prefect.schedules import IntervalSchedule
from prefect.engine.executors import DaskExecutor


@task
def make_error():
    print("no")


schedule = IntervalSchedule(
    start_date=datetime.utcnow() + timedelta(seconds=1), interval=timedelta(minutes=1)
)

with Flow("Hello", schedule) as flow:
    make_error()

flow.run(executor=DaskExecutor(address="tcp://localhost:8786"))
