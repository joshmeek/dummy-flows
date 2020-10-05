from prefect import task, Flow, triggers
from prefect.engine.results import LocalResult

@task
def task_1(result=LocalResult()):
    return 1

@task(trigger=triggers.manual_only, result=LocalResult())
def add_one(x):
    return x + 1

with Flow("example", result=LocalResult()) as flow:
    t1 = task_1()
    t2 = add_one(x=t1)

flow.register(project_name="Demo")

flow.run_agent()