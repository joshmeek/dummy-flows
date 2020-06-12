import os
import prefect
from prefect import task, Flow
from prefect.environments.storage import Docker
from prefect.environments.storage import S3
from prefect.engine.results.s3_result import S3Result

@task
def add(x, y=1):
    """
    The only task we use so far here ;-)
    """
    logger = prefect.context.get("logger")
    logger.info("Hello from add(x,y)!")
    return x + y

def create_flow():
    """
    Create the flow
    """
    result = S3Result(
        bucket="my-prefect-flows",
    )

    with Flow("Sample Flow #1", result=result) as flow:
        first_result = add(1, y=2)
        second_result = add(x=first_result, y=100)

    storage = Docker(
        base_image="prefecthq/prefect:0.11.5-python3.7",
        image_name="sample-flow",
        image_tag="test2",
        python_dependencies=["boto3"],
        prefect_version="master",
        build_kwargs=dict(),
    )
    storage.add_flow(flow)
    flow.storage = storage
    return flow

f = create_flow()
f.register()