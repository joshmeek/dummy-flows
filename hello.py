import prefect
from prefect import task, Flow
from prefect.environments.storage import Docker

@task
def hello_task():
    logger = prefect.context.get("logger")
    logger.info("Hello, Cloud!")
flow = Flow("hello-flow", tasks=[hello_task])

flow.storage = Docker(registry_url="docker.io/joshmeek18")
flow.register(project_name="Hello, World!")