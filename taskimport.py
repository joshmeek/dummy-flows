from prefect import task

@task
def my_task():
    return 43