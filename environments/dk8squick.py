from prefect import task, Flow
from prefect.environments import DaskKubernetesEnvironment, LocalEnvironment
from prefect.environments.storage import Docker
import time


@task
def get_value():
    time.sleep(10)
    return "Example!"


@task
def output_value(value):
    print(value)


with Flow(
    "local-dask-k8s",
    environment=DaskKubernetesEnvironment(min_workers=2, max_workers=4),
    storage=Docker(registry_url="joshmeek18", image_name="flows", prefect_version="master"),
) as flow:
    get_value()
    get_value()
    get_value()
    get_value()
    get_value()
    get_value()
    get_value()
    get_value()
    get_value()
    get_value()
    get_value()

from prefect.engine.executors import DaskExecutor

# flow.environment = LocalEnvironment(
#     executor=DaskExecutor(
#         min_workers=2,
#         max_workers=4
#         # cluster_kwargs={"n_workers": 0, "threads_per_worker": 1, "silence_logs": 10},
#         # adapt_kwargs={"minimum": 1, "maximum": 3},
#     )
# )

flow.register("Demo")
# flow.run(executor=DaskExecutor(address="localhost:8786"))

