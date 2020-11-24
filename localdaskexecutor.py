from prefect import task, Flow
from prefect.environments import LocalEnvironment
from prefect.engine.executors import LocalDaskExecutor

@task
def vals():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

@task
def printv(v):
    print(v)

with Flow("local-dask", environment=LocalEnvironment(executor=LocalDaskExecutor(nthreads=4))) as f:
    v = vals()
    printv.map(v)

f.register(project_name="Demo")