from prefect import task
from prefect.engine.results import S3Result
import time

@task(target="{task_name}-{today}")
def extract():
    """Get a list of data"""
    return [1, 2, 3]


@task(target="{task_name}-{today}")
def transform(data):
    """Multiply the input by 10"""
    return [i * 10 for i in data]


@task
def load(data):
    """Print the data to indicate it was received"""
    print("Here's your data: {}".format(data))


from prefect import Flow

with Flow("ETL", result=S3Result(bucket="")) as flow:
    e = extract()
    t = transform(e)
    l = load(t)

flow.run()
