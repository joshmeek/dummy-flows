from prefect import task, Flow
import prefect

list = [1, 2]


@task
def foo(x):
    print(f"Index: {prefect.context.map_index}")
    print(x)


with Flow("foo") as flow:
    foo.map(x=list)

flow.run()
