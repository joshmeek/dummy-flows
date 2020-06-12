from prefect import task, Flow
from prefect.environments import RemoteEnvironment
import time


@task
def get_data():
    return [x for x in range(10)]


@task
def multiply(x):
    if x == 9:
        time.sleep(20)
    time.sleep(1)
    return x * 10


@task
def divide(x):
    time.sleep(1)
    return x / 10


@task
def reduce(vals):
    print(sum(vals))


with Flow("mlm") as flow:
    data = get_data()
    m = multiply.map(data)
    d = divide.map(m)
    m2 = multiply.map(d)
    d2 = divide.map(m2)
    reduce(d2)


flow.environment = RemoteEnvironment(executor="prefect.engine.executors.DaskExecutor")
flow.register(project_name="Demo")
