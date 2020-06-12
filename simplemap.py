from prefect import task, Flow
from prefect.triggers import any_successful


@task
def multiply(x):
    return 10 * x


@task(trigger=any_successful)
def aggregate(results):
    print(results)


with Flow("divide-fail") as flow:
    results = multiply.map([0, 1, 2])
    aggregate(results)

flow.register(project_name="Demo")