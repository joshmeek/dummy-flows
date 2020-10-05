from prefect import task, Flow
from prefect.tasks.docker import (
    CreateContainer,
    StartContainer,
    GetContainerLogs,
    WaitOnContainer,
)

create = CreateContainer(image_name="prefecthq/prefect", command="echo 12345")
start = StartContainer()
wait = WaitOnContainer()
logs = GetContainerLogs()


@task
def see_output(out):
    print(out)


with Flow("docker-flow") as flow:
    container_id = create()
    s = start(container_id=container_id)
    w = wait(container_id=container_id)

    l = logs(container_id=container_id)
    l.set_upstream(w)

    see_output(l)

flow.run()
