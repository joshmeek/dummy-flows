
from prefect import task, Flow
from prefect.tasks.secrets import PrefectSecret

@task
def my_value(x):
    print(x)

with Flow("f") as f:
    v = PrefectSecret("MY_SECRET")
    a = my_value(8)
    my_value(v, upstream_tasks=[a])

f.run()