from prefect import Flow, task
from prefect.triggers import any_failed


@task
def sleep_me():
    import time

    time.sleep(300)
    return "300"


@task(trigger=any_failed)
def should_i_run(x):
    print(x)
    print("I was able to run")


with Flow("long-sleep") as flow:
    s = sleep_me()
    should_i_run(s)

flow.register(project_name="Demo")
