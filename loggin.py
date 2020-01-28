import prefect
from prefect import Flow, task


@task
def log_me():
    logger = prefect.context.get("logger")
    logger.info("LOGGED")
    return "LOGGER"

with Flow("loggin") as flow:
    log_me()

flow.register(project_name="Demo")