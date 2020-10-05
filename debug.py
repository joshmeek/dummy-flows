from prefect import task, case, Flow, Parameter
from prefect import task, Flow, Parameter
import itertools


@task
def cross_product(x, y) -> list:
    print(list(itertools.product(x, y)))
    return list(itertools.product(x, y))


@task
def concat(a) -> str:
    return a[0] + a[1]


a = ["d", "o", "g"]
b = ["c", "a", "t"]

with Flow(name="zip-map-test") as flow:
    cross_result = cross_product(a, b)
    result = concat.map(cross_result)

st = flow.run()
st.result[concat].result
