from prefect import task, Flow
from prefect.engine.executors import DaskExecutor
from prefect.environments import RemoteEnvironment

@task
def values():
    return [i for i in range(100)]

@task
def pvals(x):
    print(x)

with Flow('bigmap') as f:
    vals = values()
    pvals.map(vals)

f.environmet = RemoteEnvironment(executor="prefect.engine.executors.DaskExecutor")
f.register()

# if __name__ == "__main__":
#     f.run(executor=DaskExecutor())