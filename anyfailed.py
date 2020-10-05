from prefect import task, Flow
from prefect.triggers import any_failed
from prefect.engine.signals import FAIL

@task
def a():
    raise FAIL

@task(trigger=any_failed)
def b():
    return

@task(trigger=any_failed)
def c():
    return

with Flow('f') as f:
    a = a()
    b = b()
    c = c()
    f.chain(a, b, c)

f.run()