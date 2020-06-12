
from prefect import Task, Flow, task
from prefect.engine.results import LocalResult

@task(target="{task_name}-{today}-5")
def get_data():
    """test"""
    return [1, 2, 3, 4, 5]

@task
def print_data(data):
    print(data)


with Flow("using-targets", result=LocalResult(), ) as flow:
    data = get_data()
    print_data(data)

flow.run()
# flow.register(project_name="Demo")

# class GetData(Task):
#     def run(self):
#         print(1)

# GetData()

# get_data()