import os

import boto3
from prefect import Parameter, Flow, task
from prefect.environments import LocalEnvironment
from prefect.environments.storage import S3


# testing boto directly
s3 = boto3.resource("s3")

for bucket in s3.buckets.all():
    print(bucket.name)



# testing boto via Prefect
@task
def say_hello(person: str) -> None:
    print("Hello, {}!".format(person))


with Flow("Say hi!") as flow:
    name = Parameter("name")
    say_hello(name)


storage = S3(bucket="my-prefect-flows")
# also tried, after setting AWS_CREDENTIALS:
# storage = S3(bucket="REDACTED", secrets=["AWS_CREDENTIALS"])


flow.storage = storage


flow.register(project_name="Demo")