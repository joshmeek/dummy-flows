from prefect import Flow, task
from prefect.environments.storage import Docker


@task
def get_num():
    return 5


@task
def do_nothing(x):
    print(x)


with Flow("Flow 1", storage=Docker()) as flow:
    num = get_num()
    do_nothing(num)

flow.register(project_name="Demo")
