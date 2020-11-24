import os
from typing import List

import prefect
from prefect import Flow, task
from prefect.engine.results import LocalResult


@task(name="A")
def task_a() -> List[int]:
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@task(name="B")
def task_b(foo: List) -> None:
    prefect.context.logger.info(f"Task B {foo}")


@task(name="C")
def task_c(foo: List[int]) -> None:
    prefect.context.logger.info(f"Task C {foo}")


# result_directory = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "..", "results")
# )

result = LocalResult(
    # dir=result_directory,
    location="{flow_name}/"
    "{scheduled_start_time:%d-%m_%H-%M-%S}/"
    "{task_full_name}-{task_run_id}.prefect_result",
)

with Flow(name="multilineresult", result=result) as flow:
    a = task_a()
    b = task_b(a)
    c = task_c(a)

    # Commenting out this line removes the state dependency and the flow works
    # just fine
    flow.set_dependencies(task=c, upstream_tasks=[b])

flow.register(project_name="Demo")