from prefect import task, Flow
from prefect.engine.signals import FAIL
from prefect.environments import RemoteDaskEnvironment

@task(name="yes")
def a():
    pass

@task(name="no")
def b():
    raise FAIL

@task(name="maybe so")
def c():
    print("I'm good")

with Flow("rde", environment=RemoteDaskEnvironment(address="not-real-address:8786")) as flow:
    a = a()
    b = b()
    c = c()

    c.set_upstream(a)
    c.set_upstream(b)

flow.register("Demo")