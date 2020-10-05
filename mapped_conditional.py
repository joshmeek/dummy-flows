from prefect import Flow, task
from prefect.tasks.control_flow import FilterTask, ifelse, merge, switch, case

@task
def identity(x):
    return x

with Flow("test") as flow:
    producer = identity.copy().bind(["a", "b"])

    cond = identity.copy().bind(producer, mapped=True)

    a = identity.copy().bind("a")
    a.set_upstream(producer, mapped=True)

    b = identity.copy().bind("b")
    b.set_upstream(producer, mapped=True)

    c = identity.copy().bind("c")
    c.set_upstream(producer, mapped=True)

    switch(cond, cases=dict(a=a, b=b, c=c), mapped=True)

    d = merge(a, b, mapped=True)

# state = flow.run()

# assert state.result[cond].result == ["a", "b"]
# assert state.result[a].result == ["a", None]
# assert state.result[b].result == [None, "b"]
# assert state.result[c].result == [None, None]
# assert state.result[d].result == ["a", "b"]

@task
def get_data():
    return [1, 2, 3, 4]

with Flow("maptest") as flow:
    data = get_data()
    switch()