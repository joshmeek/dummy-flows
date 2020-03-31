import prefect
from prefect import Flow, task
import time

@task
def log_me():
    time.sleep(10)
    logger = prefect.context.get("logger")
    logger.info("LOGGED")
    return "LOGGER"

with Flow("loggin") as flow:
    log_me()

flow.register(project_name="Demo")