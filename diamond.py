import prefect
import datetime


class FailOnceTask(prefect.Task):
    def __init__(self, name):
        super().__init__(
            name=name, retry_delay=datetime.timedelta(seconds=0), max_retries=1
        )

    def run(self):
        if prefect.context.task_run_count <= 1:
            raise ValueError("Run me again!")


flow = prefect.Flow("Diamond",)

flow.a = FailOnceTask("a")
flow.b = FailOnceTask("b")
flow.c = FailOnceTask("c")
flow.d = FailOnceTask("d")

flow.add_edge(flow.a, flow.b)
flow.add_edge(flow.a, flow.c)
flow.add_edge(flow.b, flow.d)
flow.add_edge(flow.c, flow.d)

flow.register("Demo")
