from prefect import Flow, task
from prefect.engine import signals


@task
def task1():
    raise signals.FAIL


@task
def task2():
    raise signals.FAIL

    return "input"


@task
def task3(input):
    print(input)


with Flow("restart-multiple-roots") as flow:
    task1()

    result1 = task2()
    task3(result1)

flow.register(project_name="Demo")