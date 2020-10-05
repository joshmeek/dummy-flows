import prefect
print(prefect.__version__)

from prefect import task, Flow
from prefect.engine.results import S3Result

@task(target="{task_name}-{today}")
def extract():
    return [1, 2, 3]

@task(target="{task_name}-{today}")
def transform(data):
    return [i * 10 for i in data]

@task
def load(data):
    print("Here's your data: {}".format(data))

with Flow("ETL", result=S3Result(bucket="prefect-test-bucket")) as flow:
    e = extract()
    t = transform(e)
    l = load(t)

flow.run()