import random
import prefect
from prefect import Flow, task
from prefect.environments.storage import Docker
from prefect.environments import RemoteEnvironment, DaskKubernetesEnvironment


@task
def numbers_task():
    n = random.randint(10, 50)
    return list(range(n))


@task
def map_task(x):
    import logging
    logger = logging.getLogger('TEST')
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

    logger.debug("DEBUG")
    logger.info("INFO")
    logger.critical("CRITICAL")
    return x + 1


@task
def reduce_task(x):
    logger = prefect.context.get("logger")
    logger.info(sum(x))


with Flow(
    "Map / Reduce dk8s",
    storage=Docker(
        registry_url="joshmeek18", image_name="flows", prefect_version="extraloggers"
    ),
    # environment=RemoteEnvironment(
    #     executor="prefect.engine.executors.DaskExecutor",
    #     executor_kwargs={"address": "tcp://dask-scheduler:8786"},
    # ),
    environment=DaskKubernetesEnvironment(),
) as flow:
    numbers = numbers_task()
    first_map = map_task.map(numbers)
    second_map = map_task.map(first_map)
    reduction = reduce_task(second_map)

flow.register(project_name="QA")
