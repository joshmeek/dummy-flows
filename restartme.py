from datetime import timedelta

from prefect import Flow, task
from prefect.engine.executors import DaskExecutor, LocalDaskExecutor
from prefect.environments import LocalEnvironment
from prefect.engine.results import LocalResult
from prefect.environments.storage import Local


@task
def generate_list():
    return [1, 2, 3]


@task
def do_something(n):
    return n


@task
def fail(x):
    print(x)
    raise ValueError()


result = LocalResult(location="{task_full_name}.pb")
with Flow(
    "Restart Me",
    storage=Local(
        stored_as_script=True,
        path="/Users/josh/Desktop/code/Dummy-Flows/restartme.py",
    ),
    result=result,
) as flow:
    lst = generate_list()
    d = do_something.map(lst)
    fail(d)

environment = LocalEnvironment(executor=DaskExecutor())
flow.environment = environment
