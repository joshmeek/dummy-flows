from prefect import Flow, task
from prefect.environments.storage import S3


@task
def extract():
    return [1, 2, 3]


@task
def transform(data):
    return [i * 10 for i in data]


@task
def load(data):
    print("Here's your data: {}".format(data))



with Flow(
    "ETL-s3-reg-demo",
    storage=S3(bucket="my-prefect-flows", secrets=["AWS_CREDENTIALS"],)
) as flow:
    e = extract()
    t = transform(e)
    l = load(t)

flow.register(project_name="Demo")
# print(flow_id)