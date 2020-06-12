from prefect import Flow, task, unmapped, Parameter
from prefect.engine.results import LocalResult
from prefect.engine.executors import LocalDaskExecutor, DaskExecutor
from prefect.engine.cache_validators import all_parameters

lr = LocalResult(
    location="{flow_name}-{task_name}-{x}-{y}.pkl", validators=all_parameters
)


@task(log_stdout=True, checkpoint=True)
def add(x, y):
    print(f"add ran with {x} {y}")
    try:
        return sum(x) + y
    except TypeError:
        return x + y


with Flow("iterated map", result=lr) as flow:
    y = unmapped(Parameter("y", default=7))
    x = Parameter("x", default=[1, 2, 3])
    mapped_result = add.map(x, y=y)
    out = add(mapped_result, y)

if __name__ == "__main__":
    flow.run(executor=DaskExecutor())
