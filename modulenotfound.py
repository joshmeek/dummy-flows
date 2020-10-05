from asdfghjk import my_module
from asdfghjk2 import my_module2
from taskimport import my_task
from prefect import task, Flow
from prefect.environments.storage import Docker


@task
def get_value(x):
    print(my_module())
    print(my_module2())
    print(x)


with Flow("modulenotfound") as flow:
    v = my_task()
    get_value(v)

flow.storage = Docker(
    files={
        "/Users/josh/Desktop/code/Dummy-Flows/asdfghjk.py": "/modules/asdfghjk.py",
        "/Users/josh/Desktop/code/Dummy-Flows/asdfghjk2.py": "/modules/asdfghjk2.py",
    },
    # env_vars={"PYTHONPATH": "$PYTHONPATH:modules/"},
)

# flow.run()
flow.register(project_name="Demo")
