import prefect
from prefect import task, Flow
from prefect.engine.results import LocalResult

# prefect.config.flows.checkpointing = True


@task(result=LocalResult(location="test.prefect"))
def test():
    print("Hello!")
    return 1


with Flow("test") as flow:
    test()
flow.run()
