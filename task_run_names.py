
from prefect import task, Flow

@task
def get_values():
    return ['a', 's', 'd', 'f']

@task(log_stdout=True, task_run_name=lambda **kwargs: f"{kwargs['v']}")
def idk(v):
    print(v)

with Flow("task_run_names") as flow:
    vals = get_values()
    idk.map(vals)

flow.register(project_name="Demo")