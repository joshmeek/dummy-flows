from prefect import task, Flow
from prefect.environments.storage import Docker


@task
def add(x, y):
    return x + y


with Flow(
    "dockerfile-test",
    storage=Docker(
        dockerfile="Dockerfiles/Dockerfile"
    ),
) as flow:
    add(1, 2)

flow.register(project_name="Demo")
