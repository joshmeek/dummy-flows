from prefect import task, Flow

@task
def t():
    pass

@task
def r(x):
    pass

with Flow("demo") as f:
    a = t()
    a2 = r(a)
    r(a)
    r(a)
    r(a)

    b = t()
    b2 = r(b)
    r(b)
    r(b)
    r(b)

f.visualize()