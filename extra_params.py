from prefect import Flow, Parameter
from prefect.schedules import Schedule
from prefect.schedules.clocks import CronClock

a = Parameter('a', default=None, required=False)
b = Parameter('b', default=None, required=False)

schedule = Schedule(clocks=[
    CronClock(' 0 18  *  *  6', parameter_defaults={'a': 'a', 'b': 'b'}),
    CronClock(' 0 12  *  *  0', parameter_defaults={'a': 'a', 'b': 'b'})
])

flow = Flow(
    name='test flow', schedule=schedule
)

# flow.add_task(a)
# flow.add_task(b)

flow.register(project_name="Demo")