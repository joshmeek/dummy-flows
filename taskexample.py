from prefect import Task, Flow, task

@task
def get_value_1():
    return 100

@task
def get_value_2():
    return 200

class MyTask(Task):
    def __init__(self, val = None, **kwargs):
        self.val = val
        super().__init__(**kwargs)

    def run(self, val = None):
        print(self.val or val)

my_task = MyTask()

with Flow("task-with-default") as flow:
    t1 = my_task(get_value_1())
    t2 = my_task(get_value_2())

flow.run()