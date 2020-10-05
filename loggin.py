import prefect
from prefect import Flow, task
import time
from datetime import timedelta

@task(timeout=11)
def log_me():
    logger = prefect.context.get("logger")
    logger.info("LOGGED")
    return "LOGGER"

with Flow("loggin") as flow:
    log_me()

from prefect.environments import LocalEnvironment
from prefect.engine.executors import DaskExecutor

flow.environment=LocalEnvironment(executor=DaskExecutor())

flow.register(project_name="Demo")