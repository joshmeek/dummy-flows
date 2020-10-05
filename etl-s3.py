from prefect import Flow, task
from prefect.environments.storage import S3


@task
def extract():
    """Get a list of data"""
    return [1, 2, 3]


@task
def transform(data):
    """Multiply the input by 10"""
    return [i * 10 for i in data]


@task
def load(data):
    """Print the data to indicate it was received"""
    # import random
    # i = random.randint(0, 5)
    # if i != 3:
    #     raise ValueError("The three is not for me.")

    print("Here's your data: {}".format(data))



with Flow(
    "ETL-s3",
    storage=S3(bucket="my-prefect-flows", secrets=["AWS_CREDENTIALS"])
) as flow:
    e = extract()
    t = transform(e)
    l = load(t)

flow_id = flow.register(project_name="Demo")
# print(flow_id)