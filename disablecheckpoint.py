from prefect import task, Flow, Parameter
from prefect.engine.result import NoResult

@task()
def vals():
    return [1, 2, 3]

@task()
def ret(x):
    return 1

with Flow('a') as f:
    p = Parameter('p')
    v = vals()
    a = ret.map(v)
    b = ret.map(p)

f.register(project_name="Demo")