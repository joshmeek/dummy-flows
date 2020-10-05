from prefect import Flow, task
from prefect.environments import LocalEnvironment
from prefect.environments.storage import S3


@task
def do_it():
    return 1


# storage = Docker(
#     image_name="test_image",
#     image_tag="latest",
#     python_dependencies=["boto3"]
# )

# storage.build()

with Flow(
    "simple-s3-storage",
    storage=S3(bucket="my-prefect-flows", secrets=["AWS_CREDENTIALS"]),
    environment=LocalEnvironment(
        metadata={"image": "test_image:latest"}
    ),
) as flow:
    x = do_it()

flow.register(project_name="Demo")
