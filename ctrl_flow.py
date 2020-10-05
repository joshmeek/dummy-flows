import prefect
from prefect import Flow, Task, task
from prefect.engine.result import NoResult
from prefect.engine.state import Skipped, Success
from prefect.tasks.control_flow import FilterTask, ifelse, merge, switch
from prefect.utilities.tasks import as_task


class Condition(Task):
    def run(self):
        return prefect.context.CONDITION


@task
def identity(x):
    return x


condition = Condition()

with Flow(name="test") as flow:
    true_branch = identity("true")
    false_branch = identity("false")
    res = ifelse(condition, true_branch, false_branch)
    assert len(flow.tasks) == 7

with prefect.context(CONDITION=False):
    state = flow.run()
