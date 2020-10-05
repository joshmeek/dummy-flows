import prefect
from prefect import Flow, task
from prefect.engine.executors import LocalDaskExecutor, DaskExecutor
from prefect.engine.state import Failed
from prefect.environments import LocalEnvironment
from prefect.utilities.notifications import slack_notifier

flow_name = "logger-test"


@task(timeout=60 * 60 * 2)
def test():
    from prefect import context
    logger = context.get("logger")
    logger.info("this is a test")


with Flow(
    flow_name,
    environment=LocalEnvironment(LocalDaskExecutor()),
    # state_handlers=[slack_notifier(only_states=[Failed])],
) as flow:
    test()
flow.register("Demo")

