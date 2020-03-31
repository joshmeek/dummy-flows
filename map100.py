from prefect import task, Flow
from prefect.environments.storage import Docker


@task
def values():
    return [1] * 100


@task
def do_something(x):
    return x


with Flow(
    "map_100_docker",
    storage=Docker(
        registry_url="joshmeek18",
        image_name="flows",
    ),
) as flow:
    v = values()
    do_something.map(v)

flow.register(project_name="QA")

