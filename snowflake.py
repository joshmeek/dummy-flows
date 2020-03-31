from prefect import Flow, task
from prefect.tasks.secrets import Secret
from prefect import Task


@task
def arg(x):
    print(x)


class SFQ(Task):
    def run(self, **kwargs):
        print(x.run())
        super().run(**kwargs)


with Flow("snowflake-flow") as flow:
    x = Secret("TEST_SECRET")()
    SFQ(x)()

flow.run()
