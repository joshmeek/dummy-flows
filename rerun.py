import prefect
from prefect import Flow, task
from prefect.engine.results import PrefectResult
from random import random

@task
def make_data():
    return list(range(5))

@task
def randomly_raise(x):
    x = random()
    if x <= 0.5:
        raise Exception()

with Flow("test retries", result=PrefectResult()) as flow:
    data = make_data()
    randomly_raise.map(data)

flow.run()
# flow.register(project_name="Demo")