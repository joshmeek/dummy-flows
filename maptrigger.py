from prefect import task, Flow
from prefect.triggers import any_failed

@task
def values():
    return [1, 2, 3]

@task
def calculate(x):
    if x == 2:
        raise ValueError()
    return x

@task(trigger=any_failed)
def sumit(x):
    print(sum(x))

with Flow("test") as f:
    vals = values()
    x = calculate.map(vals)
    sumit.map(x)

f.run()