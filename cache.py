import datetime
from prefect import task, Flow
from prefect.engine.result_handlers import LocalResultHandler


@task(
    cache_for=datetime.timedelta(minutes=1),
    checkpoint=True,
    cache_key="test",
    result_handler=LocalResultHandler(),
)
def long_task():
    import time

    time.sleep(30)
    return 30


@task
def print_upstream(x):
    print(x)


with Flow("caching") as f:
    x = long_task()
    print_upstream(x)

f.run()
