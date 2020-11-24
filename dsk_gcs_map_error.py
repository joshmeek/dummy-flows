from datetime import timedelta
# from prefect import *
from prefect import Flow, task
from prefect.engine.executors import DaskExecutor
from prefect.environments import LocalEnvironment
from prefect.engine.results import GCSResult, LocalResult
from prefect.environments.storage import GCS
# GCSResult(bucket="prefect-flows-josh")
# storage=GCS(bucket="prefect-flows-josh")

# @task#(max_retries=1, retry_delay=timedelta(seconds=0.1))
# def generate_random_list():
#     n = 10
#     return list(range(n))

# @task#(max_retries=1, retry_delay=timedelta(seconds=0.1))
# def wait(n):
#     from time import sleep
#     sleep(n)
#     return n

# @task#(max_retries=1, retry_delay=timedelta(seconds=0.1))
# def fail(values):
#     raise ValueError(f"n: {len(values)}")
# #result=LocalResult(), storage=GCS(bucket="prefect-flows-josh"),
# with Flow("GCSTest", environment=LocalEnvironment(executor=DaskExecutor())) as TestFlow:
#     lst = generate_random_list()

#     values = wait.map(lst)
#     fail(values)


# # TestFlow.environment = LocalEnvironment(executor=DaskExecutor())
# # TestFlow.visualize()
# TestFlow.register(project_name="Demo")


@task
def generate_list():
    return [1, 2, 3]

@task
def do_something(n):
    return n

@task
def fail(values):
    raise ValueError(f"n: {len(values)}")
# environment=LocalEnvironment(executor=DaskExecutor())
with Flow("Restart Fail", result=LocalResult(location="{task_full_name}.pb"), environment=LocalEnvironment(executor=DaskExecutor())) as flow:
    lst = generate_list()
    values = do_something.map(lst)
    fail(values)

flow.register(project_name="Demo")
