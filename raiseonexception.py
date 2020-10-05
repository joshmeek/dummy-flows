from prefect import task, Flow

@task
def a():
    return 1 / 0

f = Flow('raise_on_exception', tasks=[a])

f.register(project_name="Demo2")