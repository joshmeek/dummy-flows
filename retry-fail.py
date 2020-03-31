from prefect import Flow, task
from prefect.environments.storage import S3
import datetime


@task(max_retries=1, retry_delay=datetime.timedelta(minutes=1))
def fail_me():
    raise ValueError()
    print("This will not work")



with Flow(
    "retry-fail",
) as flow:
    fail_me()

flow.register(project_name="Demo")
