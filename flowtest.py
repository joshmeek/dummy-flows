from prefect import task, Flow
from prefect.environments import RemoteEnvironment
from prefect.environments.storage import Docker


@task
def data():
    return 1


@task
def transform(x):
    return x + 1


@task(tags=['testtagherelol'])
def pdata(orig, trans):
    print(orig)
    print(trans)


with Flow(
    "testflow-fargate",
    environment=RemoteEnvironment(
        executor="prefect.engine.executors.DaskExecutor",
        executor_kwargs={'n_workers': 16},
    ),
    storage=Docker(registry_url="joshmeek18", image_name="flows"),
) as flow:
    x = data()
    t = transform(x)
    p1 = pdata(x, t)
    p2 = pdata(x, t)

# flow.run()
flow.register(project_name="Demo")
# flow.visualize()
