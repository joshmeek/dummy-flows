from prefect import Flow, task


@task
def sleep_me():
    import time

    time.sleep(600)
    return "600"


with Flow("long-sleep") as flow:
    sleep_me()

flow.register(project_name="QA")
