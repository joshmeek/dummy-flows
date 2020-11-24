
from prefect import task, Flow
from prefect.engine.signals import FAIL
from prefect.tasks.prefect import CancelFlowRunTask
from prefect.triggers import any_failed

@task
def i_am_bad():
    raise FAIL("Oh no!")

@task
def i_am_good():
    print("yes")

@task
def i_am_downstream():
    print("I should not run")

cancel_task = CancelFlowRunTask(trigger=any_failed)

with Flow("cancel_me") as flow:
    bad = i_am_bad()
    good = i_am_good()

    cancel = cancel_task(upstream_tasks=[bad, good])

    downstream = i_am_downstream(upstream_tasks=[cancel])

flow.register(project_name="Demo")