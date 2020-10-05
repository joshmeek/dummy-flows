from datetime import timedelta, datetime
from prefect import task, Flow
from prefect.schedules import IntervalSchedule


@task
def getone():
    return 1


schedule = IntervalSchedule(
    start_date=datetime.utcnow() + timedelta(seconds=1), interval=timedelta(minutes=1),
)
with Flow("testflow", schedule=schedule) as flow:
    getone()

flow.register()
