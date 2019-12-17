import pendulum
from datetime import timedelta
from prefect import task, Flow, schedules
from prefect.schedules import filters, Schedule
@task
def say_hello():
    print("hello world")

curr_schedule = Schedule(
    # Fire every min
    clocks=[schedules.clocks.IntervalClock(interval=timedelta(minutes=1), start_date=pendulum.datetime(2019, 1, 1, tz='America/New_York'))],
    # Only on weekdays
    filters=[filters.is_weekday],
    # and only at 8.15am, 9.30am, 3.50pm, 4pm
    or_filters=[
        filters.between_times(pendulum.time(hour=8, minute=15), pendulum.time(hour=8, minute=15)),
        filters.between_times(pendulum.time(hour=9, minute=30), pendulum.time(hour=9,minute=30)),
        filters.between_times(pendulum.time(hour=10, minute=37), pendulum.time(hour=10,minute=37)),
        filters.between_times(pendulum.time(hour=16), pendulum.time(hour=16)),
    ],
    # do not run on Christmas
    not_filters=[
        filters.between_dates(12, 25, 12, 25)
    ]
)

with Flow('Sounds alerts', curr_schedule) as flow:
    say_hello()

flow.run()