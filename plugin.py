import time

from prefect import Flow, task
from prefect.engine.executors import DaskExecutor
from prefect.environments import LocalEnvironment

from distributed.diagnostics.plugin import WorkerPlugin


class DaskReport(WorkerPlugin):
    def __init__(self, flow_run_id):
        self.flow_run_id = flow_run_id

    def setup(self, worker=None):
        pass

    def teardown(self, worker=None):
        from prefect import Client

        msg = """
        Lost communication with Dask worker:
            {}
        """.format(
            worker
        )
        Client().write_run_logs(
            [
                dict(
                    flow_run_id=self.flow_run_id,
                    name="DaskWorkerPlugin",
                    message=msg,
                    level="ERROR",
                )
            ]
        )


@task
def sleep_me():
    time.sleep(60)


flow = Flow("plugin-test", tasks=[sleep_me])
flow.environment = LocalEnvironment(
    executor=DaskExecutor(address="localhost:8786", plugin=DaskReport)
)

flow.register(project_name="Demo")
