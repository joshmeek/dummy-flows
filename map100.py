from prefect import task, Flow


@task
def values():
    return [1] * 100


@task
def do_something(x):
    return x


with Flow("map_100_local") as flow:
    v = values()
    do_something.map(v)

flow.register(project_name="QA")

