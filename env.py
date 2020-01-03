from prefect import task, Flow
from prefect.environments import RemoteEnvironment


@task
def get_logs():
    from prefect import context, config
    import time
    time.sleep(5)
    logger = context.get("logger")
    logger.info("INFO HERE")
    logger.debug("DEBUG HERE")


with Flow(
    "env",
    environment=RemoteEnvironment(
        executor="prefect.engine.executors.DaskExecutor",
        executor_kwargs={
            "address": "tcp://10.0.0.61:8786"  # Address of a Dask scheduler
        },
    ),
) as f:
    get_logs()
    get_logs()
    get_logs()
    get_logs()
    get_logs()
    get_logs()
    get_logs()
    get_logs()
    get_logs()
    get_logs()
    get_logs()

f.register("Demo")
