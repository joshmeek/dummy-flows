from prefect import task, Flow
from prefect.environments.storage import GitHub
from prefect.engine.results import LocalResult


@task(result=LocalResult("{today}-{task_name}-etl"))
def extract():
    return [0, 1, 2]


@task
def transform(data):
    return [100 / i for i in data]


@task(log_stdout=True)  # pylint: disable=no-value-for-parameter
def load(data):
    print("Here's your data: {}".format(data))


with Flow("filetest") as flow:
    e = extract()
    t = transform(e)
    l = load(t)

flow.storage = GitHub(repo="joshmeek/storage_test", path="/flows/etlflow.py")
