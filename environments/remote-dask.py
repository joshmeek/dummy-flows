from prefect import task, Flow
from prefect.environments import RemoteEnvironment


@task
def get_value():
    return "Example!"


@task
def output_value(value):
    print(value)


flow = Flow(
    "Dask Executor Remote Example",
    environment=RemoteEnvironment(
        executor="prefect.engine.executors.DaskExecutor",
        executor_kwargs={
            "address": "tcp://127.0.0.1:8786"  # Address of a Dask scheduler
        },
    ),
)

# set task dependencies using imperative API
output_value.set_upstream(get_value, flow=flow)
output_value.bind(value=get_value, flow=flow)
