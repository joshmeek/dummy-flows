from prefect import task, Flow
from datetime import timedelta
from prefect.schedules import IntervalSchedule
import pendulum

@task
def say_hello():
    print("Hello, world!")


schedule = IntervalSchedule(interval=timedelta(days=1), start_date=pendulum.datetime(2010, 1, 1))

with Flow("interval-schedule", schedule) as flow:
    say_hello()

flow.run(run_on_schedule=True)
# flow.register(project_name="Demo", version_group_id="custom_int")

pd = pendulum.datetime(2010, 1, 1)

pd.add(days=1)