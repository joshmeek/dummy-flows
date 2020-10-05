import os
from prefect import task, Flow
from prefect.environments.storage import Local, S3, Docker


@task
def imi():
    print("I am I am I am I am")


with Flow("docker-file") as f:
    imi = imi()

# f.storage = Local(
#     path="/Users/josh/Desktop/code/Dummy-Flows/localfile.py", stored_as_file=True
# )

# f.storage = S3(bucket="my-prefect-flows", key="flowtest.py", stored_as_file=True)

f.storage = Docker(
    path="flowtest.py",
    files={"/Users/josh/Desktop/code/Dummy-Flows/localfile.py": "flowtest.py"},
    stored_as_file=True,
    prefect_version="storage_enhancements",
)
