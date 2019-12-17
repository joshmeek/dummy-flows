import distributed
import time
from prefect import task, Flow
from prefect.environments import DaskKubernetesEnvironment
from prefect.environments.storage import Docker


@task
def add(x, y):
    with distributed.worker_client():
        time.sleep(30 * 60)
    return x + y


with Flow(
    "zombie",
    environment=DaskKubernetesEnvironment(min_workers=1, max_workers=4),
    storage=Docker(
        registry_url="joshmeek18",
        image_name="flows",
        prefect_version="0ed3129e36bb31d279407418e426b7f8ca8c1711",
    ),
) as flow:
    add(add(1, 2), add(2, 3))

flow.deploy(project_name="Demo")
