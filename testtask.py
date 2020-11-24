from prefect import task

@task
def testtask():
    print("TEST")