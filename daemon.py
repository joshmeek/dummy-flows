from prefect import Flow, task
from prefect.engine.executors.dask import LocalDaskExecutor

@task
def add_ten(x):
    return x + 10

# if __name__ == '__main__':
with Flow('simple map') as flow:
    mapped_result = add_ten.map([1, 2, 3])

executor = LocalDaskExecutor(scheduler='processes', num_workers=3)
flow.run(executor=executor)