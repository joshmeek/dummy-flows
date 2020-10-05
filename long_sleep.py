from prefect import Flow, task
from prefect.environments.storage import Docker

@task
def sleep_me():
    import time

    time.sleep(600)
    return "600"


with Flow("long-sleep", storage=Docker(registry_url="joshmeek18", image_name="flows")) as flow:
    sleep_me()

flow.register(project_name="Demo")
