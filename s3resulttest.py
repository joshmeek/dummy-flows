import os
from prefect import task, Flow
from prefect.engine.results.s3_result import S3Result
from prefect.environments.storage import Docker


@task
def add(x, y=1):
    """
    The only task we use so far here ;-)
    """
    return x + y


def create_flow():
    """
    Create the flow
    """
    result = S3Result(bucket="my-prefect-flows",)

    with Flow("Sample Flow", result=result) as flow:
        first_result = add(1, y=2)
        second_result = add(x=first_result, y=100)

    storage = Docker(image_name="asdf", image_tag="no", python_dependencies=["boto3"], secrets=["AWS_CREDENTIALS"], prefect_version="aws_creds_fix")
    storage.add_flow(flow)
    flow.storage = storage

    return flow

flow = create_flow()
flow.register(project_name="Demo")
