
from prefect import Task, Flow, task
from prefect.engine.results import LocalResult

@task(target=lambda **kwargs: str(kwargs['task_run_count']))
def get_data():
    """test"""
    return "data"

@task
def print_data(data):
    print(data)


with Flow("using-targets", result=LocalResult(), ) as flow:
    data = get_data()
    print_data(data)

flow.run()