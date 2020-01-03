from prefect import Flow, task
from prefect.tasks.cloud import FlowRunTask

flow_run_task = FlowRunTask(flow_name="ETL-s3", project_name="Demo")

with Flow(
    "FlowRunTask",
) as flow:
    flow_run_task()

flow.register(project_name="Demo")
