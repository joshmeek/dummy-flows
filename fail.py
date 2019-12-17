from prefect import Flow, Parameter, task
from prefect.tasks.core.constants import Constant
from prefect.engine.signals import FAIL

@task
def trythis(x, fail=False):
    if fail:
        raise FAIL()
    return [k+1 for k in x]

@task
def tryprint(x):
    print(x)

with Flow("math") as f:
    x = Parameter("x")
    y = trythis(x, fail=True)
    y1 = trythis(y, fail=False)
    z = tryprint.map(y1)

flow_state = f.run(x=[1,2,3,4,5,6,7])

print(flow_state.result[z].result)