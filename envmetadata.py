from prefect import task, Flow
from prefect.environments import RemoteEnvironment
from prefect.environments.storage import S3

@task
def do():
    print("here")

with Flow("env-metadata") as f:
    do()

f.storage = S3(bucket="my-prefect-flows", secrets=["AWS_CREDENTIALS"])
# f.environment = RemoteEnvironment(metadata={"image": "lcltst2"})
f.register(project_name="Demo")

# f.environment = RemoteEnvironment(metadata={"image": "testimage:latest"})
# f.environment = RemoteEnvironment()
