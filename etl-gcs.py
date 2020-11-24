from prefect import Flow, task
from prefect.environments.storage import GCS


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
    "ETL-gcs-script",
    storage=GCS(bucket="prefect-flows-josh", stored_as_script=True,)
) as flow:
    e = extract()
    t = transform(e)
    l = load(t)

# flow_id = flow.register(project_name="Demo")
# print(flow_id)