from prefect import task, Flow
import datetime
import random
from time import sleep
from prefect.environments import LocalEnvironment
from prefect.engine.executors import DaskExecutor, LocalDaskExecutor
@task
def inc(x):
    sleep(random.random() / 10)
    return x + 1
@task
def dec(x):
    sleep(random.random() / 10)
    return x - 1
@task
def add(x, y):
    sleep(random.random() / 10)
    return x + y
@task(name="sum")
def list_sum(arr):
    return sum(arr)
# executor = DaskExecutor(address="localhost:8786")
executor = LocalDaskExecutor()
with Flow("dask-example", environment=LocalEnvironment(executor=executor)) as flow:
    incs = inc.map(x=range(100))
    decs = dec.map(x=range(100))
    adds = add.map(x=incs, y=decs)
    total = list_sum(adds)
# executor = DaskExecutor(address="tcp://10.254.248.214:8786")
# flow.run(executor=executor)
flow.register("Demo")
# flow.run_agent()
